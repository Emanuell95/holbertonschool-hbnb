import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False



config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

