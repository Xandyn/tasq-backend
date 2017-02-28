# Stdlib imports

# Core Flask imports
from flask import Blueprint
# Third-party app imports

# Imports from your apps
from apps.users.views import *


users = Blueprint('users', __name__, url_prefix='/users')
users_view = ProfileView.as_view('profile_view')


users.add_url_rule(
    '/profile',
    view_func=users_view
)


invites = Blueprint('invites', __name__, url_prefix='/invites')
invites_view = InviteView.as_view('invite_view')

invites.add_url_rule(
    '',
    defaults={'code': None},
    view_func=invites_view,
    methods=['GET']
)

invites.add_url_rule(
    '',
    view_func=invites_view,
    methods=['POST', 'PUT', 'DELETE']
)
