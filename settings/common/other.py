import os

SECRET_KEY = '271JJgsa712jhFHFS123f6avs01271'

MAIN_URL = 'http://localhost:3000/'
MAIN_API_URL = 'http://localhost:5000/'
FORGOT_PASSWORD_URL = MAIN_URL + 'forgot-password/'
CHANGE_EMAIL_URL = MAIN_URL + 'change-email/'
INVITE_REG_LINK = MAIN_URL + 'invite/'
EMAIL_TEMPLATES_IMAGES = MAIN_URL + 'src/assets/images/'
INVITE_LOGIN_LINK = MAIN_URL + 'login/'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/')

REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = ''

CELERY_BROKER_URL = 'redis://localhost:6379/0'

GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_REDIRECT_URI = 'http://127.0.0.1:5000'
GITHUB_SCOPE = 'user:email'
