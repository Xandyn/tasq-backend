# -*- coding: utf-8 -*-

# Stdlib imports
import os

# Core Flask imports
from flask import Flask

# Third-party app imports
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

# Imports from your apps
from init.database import db

from apps.users.models import *
from apps.files.models import *
from apps.tasks.models import *
from apps.projects.models import *


application = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'templates'
    ),
    static_folder=os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'static'
    )
)


migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)


application.config.from_envvar('TASQ_SETTINGS', True)
application.config['BUNDLE_ERRORS'] = True
application.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
application.config['CORS_HEADERS'] = 'X-Requested-With, Content-Type'
CORS(application, supports_credentials=True)
db.init_app(application)

# trailing slashes not necessary
application.url_map.strict_slashes = False


def init():
    with application.app_context():
        from init.jwt_init import jwt
        jwt.init_app(application)

        from apps.users.urls import users, invites
        application.register_blueprint(users)
        application.register_blueprint(invites)

        from apps.projects.urls import projects
        application.register_blueprint(projects)


init()


if __name__ == '__main__':
    if application.config['NEED_LINT']:
        import subprocess
        subprocess.call([
            "flake8",
            "./",
            "--exclude",
            "migrations",
            "--ignore",
            "E501,E712,E711,F403,F405,F401"
        ])
        manager.run()
    else:
        application.run(host='0.0.0.0', threaded=False)

