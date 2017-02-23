from settings.common import *


LOG_TO_FILE = False
DEBUG = True
NEED_LINT = False
ADMIN_ENABLED = DEBUG
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = "postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**{
    'NAME': 'tasq1',
    'USER': 'tasq1',
    'PASSWORD': '1',
    'HOST': '127.0.0.1',
    'PORT': '5432'
})
