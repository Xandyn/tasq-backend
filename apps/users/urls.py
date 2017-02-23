from flask import Blueprint
from apps.users.views import *


users = Blueprint('users', __name__, url_prefix='/users')


users.add_url_rule(
    '/profile',
    view_func=ProfileView.as_view('profile_view')
)


invites = Blueprint('invites', __name__, url_prefix='/invites')

invites.add_url_rule(
    '',
    view_func=InviteView.as_view('invite_view')
)
