# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# MongoDb settings 
MONGODB_SETTINGS = {
    'db': 'db',
    'host': 'mongodb://localhost:27017/db'
}

# Secret key for signing cookies
SECRET_KEY = "----SECRET_KEY ----"

# Mail settings
MAIL_SERVER = 'smtp.company.com'
MAIL_PORT = 587
MAIL_USERNAME = 'email@company.com.br'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = 'email@company.com.br'
MAIL_USE_TLS = False
MAIL_USE_SSL = False

# Application settings
APP_SETTINGS = {
    'name': 'IPB',
    'title': '',
    'description': '',
    'keywords': '',
    'author': 'Tiago Franco', 
    'icon-short': '/static/imgs/ipb.ico',
    'icon': '/static/imgs/ipb.png'
}

# access levels with hierarchy
ACCESS = [
    'ADMINISTRATOR', #min priority
    'COORDINATOR',
    'MASTER' #max priority
]