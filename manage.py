# Stdlib imports

# Core Flask imports

# Third-party app imports

# Imports from your apps
from init.database import db
from application import application, init, manager


application.config.from_envvar('TASQ_SETTINGS')
db.init_app(application)
init()


if __name__ == '__main__':
    with application.app_context():
        manager.run()
