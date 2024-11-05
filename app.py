from flask import Flask, render_template, request, redirect, url_for, session, g, flash, jsonify
from config import Config, LANGUAGES
import pandas as pd
from datetime import datetime
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

def load_translations(lang):
    """Load translations for the specified language."""
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Fallback to Japanese if translation not found
        with open('translations/ja.json', 'r', encoding='utf-8') as file:
            return json.load(file)

def send_email_with_excel(form_data):
    """Send email notification with form data and Excel attachment."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = app.config['RECEIVER_EMAIL']
        msg['Subject'] = f"New Application Form Submission - {form_data.get('firstname', 'Unknown')} {form_data.get('surname', 'Unknown')}"

        # Add body
        body = "New application form submission received:\n\n"
        for key, value in form_data.items():
            body += f"{key}: {value}\n"
        msg.attach(MIMEText(body, 'plain'))

        # Attach Excel file
        with open(Config.EXCEL_FILE, 'rb') as f:
            excel_attachment = MIMEApplication(f.read(), _subtype='xlsx')
            excel_attachment.add_header('Content-Disposition', 'attachment', filename='applications.xlsx')
            msg.attach(excel_attachment)

        # Send email
        with smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(msg)
            
        logger.info(f"Email sent successfully for {form_data.get('firstname')} {form_data.get('surname')}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@app.route('/')
def language_select():
    """Display language selection page."""
    return render_template('language_select.html', languages=LANGUAGES)

@app.route('/form/<lang>')
def form(lang):
    """Display the application form in the specified language."""
    if lang not in LANGUAGES:
        return redirect(url_for('form', lang='ja'))
    
    session['language'] = lang
    translations = load_translations(lang)
    
    return render_template('form.html', 
                         translations=translations,
                         language=lang)  # Make sure to pass both translations and language

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission."""
    try:
        # Get form data
        form_data = request.form.to_dict()
        form_data['submission_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save to Excel
        try:
            if not os.path.exists(Config.EXCEL_FILE):
                df = pd.DataFrame(columns=form_data.keys())
                df.to_excel(Config.EXCEL_FILE, index=False)
            
            df = pd.DataFrame([form_data])
            if os.path.exists(Config.EXCEL_FILE):
                existing_df = pd.read_excel(Config.EXCEL_FILE)
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_excel(Config.EXCEL_FILE, index=False)
            logger.info(f"Data saved to Excel for {form_data.get('firstname')} {form_data.get('surname')}")
        except Exception as e:
            logger.error(f"Failed to save to Excel: {str(e)}")
            raise

        # Send email notification
        email_sent = send_email_with_excel(form_data)
        if not email_sent:
            logger.warning("Email notification failed but data was saved")

        # Return success response
        return jsonify({
            'success': True,
            'message': load_translations(session.get('language', 'ja')).get('submit_success')
        })
        
    except Exception as e:
        logger.error(f"Form submission error: {str(e)}")
        return jsonify({
            'success': False,
            'message': load_translations(session.get('language', 'ja')).get('submit_error')
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size too large error."""
    return jsonify({
        'success': False,
        'message': load_translations(session.get('language', 'ja')).get('file_too_large')
    }), 413

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html', 
                         translations=load_translations(session.get('language', 'ja')),
                         language=session.get('language', 'ja')), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html',
                         translations=load_translations(session.get('language', 'ja')),
                         language=session.get('language', 'ja')), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.TRANSLATIONS_DIR, exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    # Create empty Excel file if it doesn't exist
    if not os.path.exists(Config.EXCEL_FILE):
        df = pd.DataFrame()
        df.to_excel(Config.EXCEL_FILE, index=False)
    
    app.run(debug=True)
