from project import app, db
from flask_testing import TestCase
from flask_login import current_user
import unittest
from project.models import *


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        details = Details(
            city="Oxshott",
            age=21,
            last="luke",
            first="de Beneducci"
        )
        db.session.add(details)
        user = User(
            email="beneducciluke@gmail.com",
            password="test"
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class AccountViewsTests(BaseTestCase):

    # Ensure account page requires a login
    def test_account_requires_login(self):
        response = self.client.get('/account', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    # Ensure vote page requires a login
    def test_vote_requires_login(self):
        response = self.client.get('/vote', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    # Ensure results page requires a login
    def test_results_requires_login(self):
        response = self.client.get('/results', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)


class UsersViewsTests(BaseTestCase):


    # Ensure login page loads correctly
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure register page loads correctly
    def test_register(self):
        response = self.client.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure login page responds to correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post('/', data=dict(username="beneducciluke@gmail.com", password="test"),
                                        follow_redirects=True)
            self.assertIn(b'You were just logged in!', response.data)
            self.assertTrue(current_user.email == "beneducciluke@gmail.com")

    # Ensure login page responds to incorrect credentials
    def test_incorrect_login(self):
        with self.client:
            response = self.client.post('/', data=dict(username="wrong@gmail.com", password="wrong"),
                                        follow_redirects=True)
            self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure logout page responds to logout request
    def test_logout_works(self):
        with self.client:
            self.client.post('/', data=dict(username="beneducciluke@gmail.com", password="test"),
                             follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were just logged out', response.data)

    # Ensure logout page requires a login
    def test_logout_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    # Ensure register page responds to incorrect first name
    def test_register_first_name_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="",lastname="de Beneducci", city="oxshott", age=20, email="beneducciluke@gmail.com", password="test", repeatpassword="test"),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to incorrect last name
    def test_register_last_name_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="", city="oxshott", age=20,
                                                       email="beneducciluke@gmail.com", password="test",
                                                       repeatpassword="test"),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to incorrect city
    def test_register_city_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="", age=20,
                                                       email="beneducciluke@gmail.com", password="test",
                                                       repeatpassword="test"),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to incorrect age
    def test_register_age_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="oxshott",
                                                       email="beneducciluke@gmail.com", password="test",
                                                       repeatpassword="test"),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to incorrect email
    def test_register_email_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="oxshott", age=20,
                                                       email="", password="test",
                                                       repeatpassword="test"),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to incorrect password
    def test_register_password_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="oxshott", age=20,
                                                       email="beneducciluke@gmail.com", password="",
                                                       repeatpassword="test"),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to incorrect repeat password
    def test_register_confirm_password_required(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="oxshott", age=20,
                                                       email="beneducciluke@gmail.com", password="test",
                                                       repeatpassword=""),
                                        follow_redirects=True)
            self.assertIn(b'This field is required', response.data)

    # Ensure register page responds to passwords matching
    def test_register_confirm_password_match(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="oxshott", age=20,
                                                       email="beneducciluke@gmail.com", password="test",
                                                       repeatpassword="aaa"),
                                        follow_redirects=True)
            self.assertIn(b'Passwords must match', response.data)

    # Ensure register page responds to correct registration
    def test_register_confirm(self):
        with self.client:
            response = self.client.post('/register', data=dict(firstname="luke", lastname="de b", city="oxshott", age=20,
                                                       email="beneducciluke@gmail.com", password="testing",
                                                       repeatpassword="testing"),
                                        follow_redirects=True)
            self.assertIn(b'You were just logged in!', response.data)
            self.assertTrue(current_user.email == "beneducciluke@gmail.com")

if __name__ == '__main__':
    unittest.main()