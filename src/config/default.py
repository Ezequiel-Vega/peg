from os.path import abspath
from os.path import dirname
from os.path import join

# Directorios
BASE_DIR = dirname(dirname(abspath(__file__)))
UPLOAD_FOLDER = join(BASE_DIR, 'app', 'static', 'audios')

# Claves secretas
SECRET_KEY = 'SecretKey'

# Entonrons de la aplicacion
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

# Base de datos
SQLALCHEMY_TRACK_MODIFICATIONS = False
