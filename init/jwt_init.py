# Stdlib imports
from datetime import datetime

# Core Flask imports
from flask import jsonify, request
from flask import current_app as app

# Third-party app imports
from flask_jwt import JWT, _jwt_required, JWTError
from werkzeug.security import check_password_hash
from sqlalchemy.orm.exc import NoResultFound

# Imports from your apps
from apps.users.models import User

jwt = JWT()


def jwt_required(f):
    u"""decorate full class MethodView
        class MyApiView(MethodView):
            decorators = [jwt_required]
            def get(self):
                return 'ok'
            def post(self):
                return 'post'
    """
    def decorator(*args, **kwargs):
        _jwt_required(realm=None)
        return f(*args, **kwargs)
    return decorator


@jwt.request_handler
def custom_header_name():
    auth_header_value = request.headers.get('JWTAuthorization', None)
    auth_header_prefix = app.config['JWT_AUTH_HEADER_PREFIX']

    if not auth_header_value:
        return

    parts = auth_header_value.split()

    if parts[0].lower() != auth_header_prefix.lower():
        raise JWTError('Invalid JWT header', 'Unsupported authorization type')
    elif len(parts) == 1:
        raise JWTError('Invalid JWT header', 'Token missing')
    elif len(parts) > 2:
        raise JWTError('Invalid JWT header', 'Token contains spaces')

    return parts[1]


@jwt.auth_response_handler
def with_role(access_token, identity):
    # role = getattr(identity, 'role') or identity['role']
    return jsonify({
        'token': access_token.decode('utf-8'),
        # 'role': role
    })


@jwt.authentication_handler
def authenticate(username, password):
    try:
        user = User.query.filter(User.email == username).one()
    except NoResultFound:
        return

    if user and check_password_hash(user.password, password):
        return user
    else:
        return


@jwt.jwt_error_handler
def error_handler(error):
    result = {
        'status_code': error.status_code,
        'error': error.error,
        'description': error.description
    }
    if error.status_code == 401:
        result['email'] = error.description
    return jsonify(result), error.status_code, error.headers


@jwt.identity_handler
def identify(payload):
    try:
        user = User.query.filter(User.id == payload['user_id']).one()
    except NoResultFound:
        return None
    return user


@jwt.jwt_payload_handler
def make_payload(identity):
    iat = datetime.utcnow()
    exp = iat + app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')
    _id = getattr(identity, 'id') or identity['id']
    return {
        'exp': exp,
        'iat': iat,
        'nbf': nbf,
        'identity': _id,
        'user_id': _id
    }
