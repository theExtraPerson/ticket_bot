import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///tickets.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    PRIMARY_API_KEY = os.getenv('PRIMARY_API_KEY')
    SECONDARY_API_KEY = os.getenv('SECONDARY_API_KEY')

class ProductionConfig(Config):
    API_KEY = Config.PRIMARY_API_KEY

class DevelopmentConfig(Config):
    API_KEY = Config.SECONDARY_API_KEY

# Use the appropriate configuration based on your environment
config = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig
