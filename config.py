class Config:
    # Flask app configuration
    SECRET_KEY = 'your_secret_key_here'  # Change this to a secure random key
    
    # Email configuration
    EMAIL = 'baljir0901@gmail.com'
    APP_PASSWORD = 'imhy kosx zqgm uikl'  # Your Gmail app password
    
    # Excel file configuration
    EXCEL_FILE = 'recruitment_data.xlsx'
    
    # Supported languages
    LANGUAGES = {
        'ja': {
            'name': '日本語',
            'flag': '🇯🇵'
        },
        'en': {
            'name': 'English',
            'flag': '🇬🇧'
        },
        'mn': {
            'name': 'Монгол',
            'flag': '🇲🇳'
        },
        'vi': {
            'name': 'Tiếng Việt',
            'flag': '🇻🇳'
        }
    }
    
    # Default language
    DEFAULT_LANGUAGE = 'ja'
