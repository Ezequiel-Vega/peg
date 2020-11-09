from .default import *

HOST = '0.0.0.0'
PORT = 4000
DEBUG = True
TESTING = True

APP_ENV = APP_ENV_TESTING

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/peg_testing"
