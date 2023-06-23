import unittest
from flask import Flask
from flask_testing import TestCase
from config import create_app, db


class YourAppTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_login_route(self):
        response = self.client.get('/login')
        self.assert200(response)
        self.assert_template_used('login.html')

    def test_register_route(self):
        response = self.client.get('/register')
        self.assert200(response)
        self.assert_template_used('register.html')


if __name__ == '__main__':
    unittest.main()
