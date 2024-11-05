from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
import pandas as pd
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'

def load_translations(lang):
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Fallback to Japanese if translation not found
        with open('translations/ja.json', 'r', encoding='utf-8') as file:
            return json.load(file)

@app.route('/')
def language_select():
    return render_template('language_select.html')

@app.route('/form/<language>')
def form(language):
    if language not in ['ja', 'en', 'mn', 'vi']:
        return redirect(url_for('language_select'))
    
    # Load translations for the selected language
    translations = load_translations(language)
    session['language'] = language
    
    # Pass translations to template as 't'
    return render_template('form.html', language=language, t=translations)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = request.form.to_dict()
        form_data['submission_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save to Excel
        df = pd.DataFrame([form_data])
        if os.path.exists(Config.EXCEL_FILE):
            existing_df = pd.read_excel(Config.EXCEL_FILE)
            df = pd.concat([existing_df, df], ignore_index=True)
        df.to_excel(Config.EXCEL_FILE, index=False)
        
        # Send email
        send_email_with_excel(form_data)
        
        flash("Form submitted successfully!", 'success')
        return redirect(url_for('form', language=session.get('language', Config.DEFAULT_LANGUAGE)))
        
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred. Please try again.", 'error')
        return redirect(url_for('form', language=session.get('language', Config.DEFAULT_LANGUAGE)))

if __name__ == '__main__':
    # Create translations directory if it doesn't exist
    if not os.path.exists('translations'):
        os.makedirs('translations')
    
    app.run(debug=True)