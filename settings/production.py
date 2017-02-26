import os
from settings.common import *

LOCAL_WORKER = False
LOG_TO_FILE = True
DEBUG = False
NEED_LINT = False
SECRET_KEY = 'o821jsahjhj21y712hbasaj721g'

MAIN_URL = 'https://tasq.com/'
ADMIN_URL = 'http://admin.tasq.com/'
MAIN_API_URL = 'https://api.tasq.com/'
FORGOT_PASSWORD_URL = MAIN_URL + 'forgot-password/'
CHANGE_EMAIL_URL = MAIN_URL + 'change-email/'
INVITE_REG_LINK = MAIN_URL + 'invite/'
EMAIL_TEMPLATES_IMAGES = MAIN_URL + 'src/assets/images/'
INVITE_LOGIN_LINK = MAIN_URL + 'login/'
API_DOMAIN = 'https://api.tasq.com/'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**{
    'NAME': os.environ['RDS_DB_NAME'],
    'USER': os.environ['RDS_USERNAME'],
    'PASSWORD': os.environ['RDS_PASSWORD'],
    'HOST': os.environ['RDS_HOSTNAME'],
    'PORT': os.environ['RDS_PORT']
})
