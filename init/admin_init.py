# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports

# Third-party app imports
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Imports from your apps
from init.database import db
from apps.users.models import User


class AuthView(object):
    def is_accessible(self):
        return True


class ModelView(AuthView, ModelView):
    pass


admin = Admin()

admin.add_view(ModelView(User, db.session))
