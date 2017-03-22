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


environment_variable = 'TASQ_SETTINGS'
if os.path.isfile(os.environ.get(environment_variable, '')):
    application.config.from_envvar(environment_variable, True)
else:
    application.config.from_object('settings.base')
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

        from apps.projects.urls import projects, collaborators
        application.register_blueprint(projects)
        application.register_blueprint(collaborators)

        from apps.tasks.urls import tasks
        application.register_blueprint(tasks)


if application.config['DEBUG']:
    from init.mail_init import mail

    mail.init_app(application)
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
