from collections import namedtuple
import os

import dotenv


def is_truthy(s):
    first_char = s[0].lower()
    return first_char in ['1', 't', 'y']


'''
    Load the configuration variables from .env
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

Config = namedtuple('Config', ['name', 'default', 'converter'])

CONFIGS = [
    Config('HOST', '0.0.0.0', str),
    Config('PORT', 5000, int),
    Config('DATABASE_URL', 'mongodb://127.0.0.1:27017/hearts', str),
    Config('SECRET_KEY', 'tyhbjhgvk5r788uo3h1jnk', str),
    Config('DEBUG', 'False', is_truthy),
]


def configure(app):
    for config in CONFIGS:
        value = config.converter(os.environ.get(config.name, config.default))
        app.config[config.name] = value

    app.config['MONGO_URI'] = app.config['DATABASE_URL']
