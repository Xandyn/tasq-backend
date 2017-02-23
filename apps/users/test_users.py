# -*- coding: utf-8 -*-

# Stdlib imports
import json

# Core Flask imports

# Third-party app imports
from sqlalchemy.orm.exc import NoResultFound
from test import Test

# Imports from your apps
from apps.users.models import User


USER_REG_DATA = {
    'name': 'Tommy',
    'email': 'tommy.west19@example.com',
    'password': '123456'
}

USER_NEW_DATA = {
    'name': 'Tommy West'
}

USER_NEW_DATA_WITH_NEW_PASSWORD = {
    'name': 'Genesis Rice',
    'email': 'genesis.rice82@example.com',
    'password': 'batman1'
}

USER_REG_DATA_SHORT_PASSWORD = {
    'name': 'Tommy',
    'email': 'tommy.west19@example.com',
    'password': '123'
}

USER_REG_DATA_WITH_SAME_UPPER_EMAIL = {
    'name': 'Tommy',
    'email': 'TOMMY.WEST19@example.com',
    'password': '123456'
}


class TestRegistration(Test):
    def auth(self):
        """
            Get Auth token Headers
        """
        data = {
            'password': USER_REG_DATA['password'],
            'email': USER_REG_DATA['email']
        }
        response = self.w.post(
            '/users/auth',
            json.dumps(data),
            content_type='application/json'
        )
        access_token = response.json.get('token')
        return {'JWTAuthorization': 'JWT {}'.format(access_token)}

    def test_1(self):
        """
            Test registration user
        """

        # Simple registration
        response = self.w.post(
            '/users/profile',
            json.dumps(USER_REG_DATA),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        try:
            user = User.query.filter(
                User.email == USER_REG_DATA['email']).one()
        except NoResultFound:
            self.assertTrue(False)

        self.assertEqual(user.email, USER_REG_DATA['email'])

        # Another registration
        response = self.w.post(
            '/users/profile',
            json.dumps(USER_NEW_DATA_WITH_NEW_PASSWORD),
            content_type='application/json',
            status=200
        )
        self.assertEqual(response.status_code, 200)

        # Registration with same upper email
        response = self.w.post(
            '/users/profile',
            json.dumps(USER_REG_DATA_WITH_SAME_UPPER_EMAIL),
            content_type='application/json',
            status=403
        )
        self.assertEqual(response.status_code, 403)

        # Registration with password less than 6
        response = self.w.post(
            '/users/profile',
            json.dumps(USER_REG_DATA_SHORT_PASSWORD),
            content_type='application/json',
            status=403
        )
        self.assertEqual(response.status_code, 403)

    def test_2(self):
        """
            Auth with username and password
        """
        auth_headers = self.auth()
        response = self.w.get(
            '/users/profile',
            headers=auth_headers
        )

        self.assertEqual(response.status_code, 200)
        email = response.json.get('email')

        self.assertEqual(email, USER_REG_DATA['email'])

    def test_3(self):
        """
            Test update profile
        """
        auth_headers = self.auth()

        response = self.w.put(
            '/users/profile',
            json.dumps(USER_NEW_DATA),
            headers=auth_headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        name = response.json.get('name')

        self.assertNotEqual(name, USER_REG_DATA['name'])

        try:
            user = User.query.filter(
                User.email == USER_REG_DATA['email']).one()
        except NoResultFound:
            self.assertTrue(False)

        self.assertNotEqual(user.name, USER_REG_DATA['name'])

    def test_4(self):
        """
            Test send email after reset-password link visit
        """
        # response = self.w.post(
        #     '/users/profile/reset-password/',
        #     json.dumps({'email': USER_REG_DATA['email']}),
        #     content_type='application/json'
        # )
        #
        # self.assertEqual(response.status_code, 200)
        pass
