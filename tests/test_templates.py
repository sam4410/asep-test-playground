import pytest
import sys
sys.path.insert(0, '/path/to/your/flask/app')  # Adjust this path to your Flask app
from flask import Flask, render_template, flash
from flask_testing import TestCase

class TestTemplates(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'test_secret'
        return app

    def test_login_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed('login.html')
        self.assertIn(b'Login', response.data)
        self.assertIn(b"Don't have an account?", response.data)

    def test_signup_template(self):
        response = self.client.get('/signup')
        self.assertTemplateUsed('signup.html')
        self.assertIn(b'Sign Up', response.data)
        self.assertIn(b'Already have an account?', response.data)

    def test_dashboard_template(self):
        response = self.client.get('/dashboard')
        self.assertTemplateUsed('dashboard.html')
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Overview', response.data)

    def test_feature_template(self):
        response = self.client.get('/feature')
        self.assertTemplateUsed('feature.html')
        self.assertIn(b'Feature Page', response.data)
        self.assertIn(b'Feature Overview', response.data)

    def test_flash_message(self):
        with self.client:
            flash('This is a test message.')
            response = self.client.get('/login')
            self.assertIn(b'This is a test message.', response.data)

    def test_sticky_navbar(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'My App', response.data)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'New Order', response.data)
        self.assertIn(b'Log out', response.data)
    def test_flash_message_display(self):
        with self.client:
            flash('Welcome to the dashboard!')
            response = self.client.get('/dashboard')
            self.assertIn(b'Welcome to the dashboard!', response.data)
    def test_navigation_links(self):
        response = self.client.get('/login')
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'New Order', response.data)
        self.assertIn(b'Log out', response.data)
    def test_dashboard_content(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'Welcome to your dashboard!', response.data)
        self.assertIn(b'Recent Orders', response.data)
        self.assertIn(b'Order ID', response.data)
        self.assertIn(b'Customer', response.data)
        self.assertIn(b'Status', response.data)
        self.assertIn(b'Date', response.data)class TestTemplates(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'test_secret'
        return app

    def test_login_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed('login.html')
        self.assertIn(b'Login', response.data)
        self.assertIn(b"Don't have an account?", response.data)

    def test_signup_template(self):
        response = self.client.get('/signup')
        self.assertTemplateUsed('signup.html')
        self.assertIn(b'Sign Up', response.data)
        self.assertIn(b'Already have an account?', response.data)

    def test_dashboard_template(self):
        response = self.client.get('/dashboard')
        self.assertTemplateUsed('dashboard.html')
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Overview', response.data)

    def test_feature_template(self):
        response = self.client.get('/feature')
        self.assertTemplateUsed('feature.html')
        self.assertIn(b'Feature Page', response.data)
        self.assertIn(b'Feature Overview', response.data)

    def test_flash_message(self):
        with self.client:
            flash('This is a test message.')
            response = self.client.get('/login')
            self.assertIn(b'This is a test message.', response.data)

    def test_sticky_navbar(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'My App', response.data)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'New Order', response.data)
        self.assertIn(b'Log out', response.data)

    def test_flash_message_display(self):
        with self.client:
            flash('Welcome to the dashboard!')
            response = self.client.get('/dashboard')
            self.assertIn(b'Welcome to the dashboard!', response.data)

    def test_navigation_links(self):
        response = self.client.get('/login')
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'New Order', response.data)
        self.assertIn(b'Log out', response.data)

    def test_dashboard_content(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'Welcome to your dashboard!', response.data)
        self.assertIn(b'Recent Orders', response.data)
        self.assertIn(b'Order ID', response.data)
        self.assertIn(b'Customer', response.data)
        self.assertIn(b'Status', response.data)
        self.assertIn(b'Date', response.data)import pytest
import sys
sys.path.insert(0, '/path/to/your/flask/app')  # Adjust this path to your Flask app
from flask import Flask, render_template, flash
from flask_testing import TestCase

class TestTemplates(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'test_secret'
        return app

    def test_login_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed('login.html')
        self.assertIn(b'Login', response.data)
        self.assertIn(b"Don't have an account?", response.data)

    def test_signup_template(self):
        response = self.client.get('/signup')
        self.assertTemplateUsed('signup.html')
        self.assertIn(b'Sign Up', response.data)
        self.assertIn(b'Already have an account?', response.data)

    def test_dashboard_template(self):
        response = self.client.get('/dashboard')
        self.assertTemplateUsed('dashboard.html')
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Overview', response.data)

    def test_feature_template(self):
        response = self.client.get('/feature')
        self.assertTemplateUsed('feature.html')
        self.assertIn(b'Feature Page', response.data)
        self.assertIn(b'Feature Overview', response.data)

    def test_flash_message(self):
        with self.client:
            flash('This is a test message.')
            response = self.client.get('/login')
            self.assertIn(b'This is a test message.', response.data)

    def test_sticky_navbar(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'My App', response.data)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'New Order', response.data)
        self.assertIn(b'Log out', response.data)