from unittest import TestCase
from app.controllers import register_user, login_user, UserCreationError, UserLoginError
from app.models import User
from app import db

class BasicUnitTests(TestCase):

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_register_user(self):
        #testing a new user
        email = "test@test.com"
        password = "testpassword"
        self.assertTrue(register_user(email,password))

        # Verify that the user exists in the database
        user = User.query.filter_by(email=email).first()
        self.assertIsNotNone(user)

