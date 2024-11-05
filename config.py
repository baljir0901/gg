import os
from flask import request, g

# Define available languages
LANGUAGES = ['en', 'ja', 'mn', 'vi']

class Config:
    # Flask app configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Email configuration
    EMAIL = 'baljir0901@gmail.com'
    APP_PASSWORD = 'imhy kosx zqgm uikl'  # Your Gmail app password
    
    # Excel file configuration
    EXCEL_FILE = 'recruitment_data.xlsx'
    
    # Supported languages
    LANGUAGES = LANGUAGES
    
    # Default language
    DEFAULT_LANGUAGE = 'ja'
