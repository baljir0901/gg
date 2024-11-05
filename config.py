import os
from flask import request

class Config:
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GG-application-form-2024'
    
    # Available Languages
    LANGUAGES = ['ja', 'en', 'mn', 'vi']
    DEFAULT_LANGUAGE = 'ja'
    
    # File Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    EXCEL_FILE = os.path.join(DATA_DIR, 'applications.xlsx')
    TRANSLATIONS_DIR = os.path.join(BASE_DIR, 'translations')
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    
    # Email Credentials
    MAIL_USERNAME = 'baljir0901@gmail.com'
    MAIL_PASSWORD = 'imhy kosx zqgm uikl'
    RECEIVER_EMAIL = 'baljir0901@gmail.com'
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}
    
    # Database Configuration (if needed later)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        # Create necessary directories
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Available languages
LANGUAGES = Config.LANGUAGES

def get_locale():
    """Get the best matching language from the user's preferences"""
    # First check if language is specified in URL
    lang = request.args.get('lang')
    if lang in LANGUAGES:
        return lang
        
    # Then fall back to browser's language preferences
    return request.accept_languages.best_match(LANGUAGES) or Config.DEFAULT_LANGUAGE
