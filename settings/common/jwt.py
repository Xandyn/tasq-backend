from datetime import timedelta


JWT_EXPIRATION_DELTA = timedelta(days=365)
JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)
JWT_VERIFY_CLAIMS = ['signature', 'exp', 'nbf', 'iat']
JWT_REQUIRED_CLAIMS = ['exp', 'iat', 'nbf']
JWT_AUTH_HEADER_PREFIX = 'JWT'
JWT_AUTH_URL_RULE = '/users/auth'
JWT_AUTH_USERNAME_KEY = 'email'
JWT_AUTH_PASSWORD_KEY = 'password'
