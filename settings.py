import os

import dotenv

'''
    Load the configuration variables from .env
'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', 5000))

DATABASE_URL = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY', 'abc123')
