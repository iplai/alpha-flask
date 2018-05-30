import os


class Config(object):
    DEBUG = True
    SECRET_KEY = 'sdfsdf82347$$%$%$%$&fsdfs!!ASx+__WEBB$'
    MONGODB_SETTINGS = {
        'db': os.environ.get('DB_NAME') or 'alpha_flask',
        'host': os.environ.get('MONGO_HOST') or 'localhost',
        'port': 27017
    }
