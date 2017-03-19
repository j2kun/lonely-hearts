from collections import namedtuple
import os

import dotenv

'''
    Load the configuration variables from .env
'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

Config = namedtuple('Config', ['name', 'default', 'converter'])

CONFIGS = [
    Config('HOST', '0.0.0.0', str),
    Config('DATABASE_URL', 'http://127.0.0.1:27017', str),
    Config('DATABASE_NAME', 'hearts', str),
    Config('SECRET_KEY', 'tyhbjhgvk5r788uo3h1jnk', str),
]


def configure(app):
    for config in CONFIGS:
        value = config.converter(os.environ.get(config.name, config.default))
        app.config[config.name] = value
