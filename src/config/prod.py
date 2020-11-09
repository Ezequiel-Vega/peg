import os
from .default import *

HOST = '0.0.0.0'
PORT = 3000
DEBUG = False

APP_ENV = APP_ENV_PRODUCTION

USER_DATABASE = os.environ.get('USER_DATABASE', 'postgres')
PASSWORD_DATABASE = os.environ.get('PASSWORD_DATABASE', 'postgres')
HOST_DATABASE = os.environ.get('HOST_DATABASE', 'localhost')
NAME_DATABASE = os.environ.get('NAME_DATABASE', 'test')
PORT_DATABASE = os.environ.get('PORT_DATABASE', 5432)

SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DATABASE}:{PASSWORD_DATABASE}@{HOST_DATABASE}:{PORT_DATABASE}/{NAME_DATABASE}"
