import os

# Base configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///book.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    
    # Login settings
    LOGIN_DISABLED = False
    
    # Pagination
    POSTS_PER_PAGE = 20

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True

# Production configuration
class ProductionConfig(Config):
    DEBUG = False

# Choose configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}