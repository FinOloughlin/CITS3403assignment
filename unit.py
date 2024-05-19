from unittest import TestCase
from app.config import TestConfig
from app.controllers import register_user, login_user, UserCreationError, UserLoginError
from app.models import User
from app import create_app, db

class BasicUnitTests(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user_success(self):
        # Testing a new user
        email = "test@test.com"
        password = "testpassword"
        self.assertTrue(register_user(email,password))

        # Verify that the user exists in the database
        user = User.query.filter_by(email=email).first()
        self.assertIsNotNone(user)
        print("User registered successfully.")
        print("User Email:", user.email)
        print("User Password:", user.password)

    def test_register_user_existing_email(self):
        # Testing an existing user
        email = "test@test.com"
        password = "testpassword"
        register_user(email, password)
        with self.assertRaises(UserCreationError, msg="User already exists"):
            register_user(email, password)

    def test_login_user_success(self):
        # Test logging in with real account
        email = "test@test.com"
        password = "testpassword"
        register_user(email, password)
        self.assertTrue(login_user(email, password))

    def test_login_user_invalid(self):
        # Test logging in with invalid details
        bademail = "fake@test.com"
        badpassword = "fake"
        email = "real@test.com"
        password = "real"
        register_user(email, password)
        self.assertFalse(login_user(bademail, badpassword))

    def test_login_user_invalid_password(self):
        # Test logging in with valid email, but invalid password
        fakeemail = "fake@test.com"
        password = "testpassword"
        email = "real@test.com"
        register_user(email,password)
        self.assertFalse(login_user(fakeemail, password))



