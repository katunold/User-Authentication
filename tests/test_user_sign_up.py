"""
Module handles tests for user sign up
"""
import json
from unittest import TestCase

from api.config.config import TestingConfig
from database.database import DatabaseConnection
from run import APP


class TestUserSignUp(TestCase):
    """
    Class with methods to test user sign up
    """

    def setUp(self):
        APP.config.from_object(TestingConfig)
        self.client = APP.test_client
        self.database = DatabaseConnection()
        self.database.init_db(APP)
        self.token = None

    def tearDown(self):
        self.database.drop_test_schema()

    def register_user(self, user_name=None, email=None,
                      password=None, user_type=None):
        return self.client().post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                user_name=user_name,
                email=email,
                password=password,
                user_type=user_type
            )),
            content_type="application/json"
        )

    def test_fine_user_registration(self):
        """
        Test for user registration
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', 'qwerty', 'client')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'success')
        self.assertTrue(received_data['message'] == 'Successfully registered')
        self.assertTrue(received_data['data']['user_type'] == 'client')
        self.assertTrue(register.content_type == 'application/json')
        self.assertEqual(register.status_code, 201)

    def test_fine_admin_registration(self):
        """
        Test for user registration
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', 'qwerty', 'admin')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'success')
        self.assertTrue(received_data['message'] == 'Successfully registered')
        self.assertTrue(received_data['data']['user_type'] == 'admin')
        self.assertTrue(register.content_type == 'application/json')
        self.assertEqual(register.status_code, 201)

    def test_missing_fields_during_signup(self):
        """
        Test for missing fields during user registration
        :return:
        """
        register = self.client().post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                user_name='Arnold',
                email='arnold@gmail.com',
                password='qwerty',
            )),
            content_type="application/json"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "This field/fields are missing")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_data_type(self):
        """
        Test user registration with invalid data-type
        :return:
        """
        register = self.register_user(13421516, 'arnold@gmail.com', 'qwerty', 'admin')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'fail')
        self.assertTrue(received_data['error_message'] == 'Only string data type supported for all fields')
        self.assertFalse(received_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_empty_fields_during_signup(self):
        """
        Test for empty fields during user registration
        :return:
        """
        register = self.register_user(' ', 'arnold@gmail.com', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "user_name is a required field")
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_password_length(self):
        """
        Test for password less than 6 characters
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', 'qwer', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] ==
                        "Password is wrong. It should be at-least 6 characters long, and alphanumeric.")
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_email_registration(self):
        """
        Test for registration with invalid email
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_email_exists(self):
        """
        Test when the user name already exists
        :return:
        """
        self.register_user('Arnold', 'arnold@gmail.com', 'qwerty', 'admin')
        register = self.register_user('Katumba', 'arnold@gmail.com', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "email already exists")
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 409)

    def test_register_with_invalid_user_type(self):
        """
        testing invalid contact
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', 'qwerty', 'guest')
        data = json.loads(register.data.decode())
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])
        self.assertEqual(register.status_code, 400)
        self.assertTrue(register.content_type, 'application/json')

    def test_invalid_user_name(self):
        """
        testing invalid contact
        :return:
        """
        register = self.register_user('Arnold94', 'arnold@gmail.com', 'qwerty', 'admin')
        data = json.loads(register.data.decode())
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])
        self.assertEqual(register.status_code, 400)
        self.assertTrue(register.content_type, 'application/json')
