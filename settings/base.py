from settings.common import *


LOG_TO_FILE = False
DEBUG = True
NEED_LINT = False
ADMIN_ENABLED = DEBUG
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = "postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**{
    'NAME': 'tasq',
    'USER': 'tasq',
    'PASSWORD': 'tasq',
    'HOST': '127.0.0.1',
    'PORT': '5432'
})
