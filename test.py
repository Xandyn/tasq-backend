# -*- coding: utf-8 -*-
from unittest import TestCase
from flask_webtest import TestApp
from flask_pytest import FlaskPytest

from application import application, init

from init.database import db

application.config.from_envvar('TASQ_TEST_SETTINGS', True)
app = FlaskPytest(application)
db.init_app(app)


class Test(TestCase):
    def setUp(self):
        self.app = app
        self.app_context = app.app_context()
        self.app_context.push()
        self.w = TestApp(self.app)

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token


init()


if __name__ == '__main__':

    with app.app_context():
        db.drop_all()
        db.create_all()
        app.run(host='127.0.0.1', port=5001)
