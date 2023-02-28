import unittest
from .. import create_app
from ..config.config import config_dict
from ..utilities import db
from ..models.users import User
from werkzeug.security import generate_password_hash



class UserTestCase(unittest.TestCase):
  
  def setUp(self):

    self.app = create_app(config_app=config_dict['test'])

    self.appctx = self.app.app_context()

    self.appctx.push()    # creates an app context

    self.client = self.app.test_client()

    db.create_all()       #creating tables for testing



  def tear_down(self):    # the reset before recreation
    db.drop_all()         # drops all existing tables in the db

    self.appctx.pop()     # removes an app context

    self.app = None

    self.client = None



  def test_user_registration(self):

    data = {
      "username": "test_user",
      "email": "test_user@gmail.com",
      "password": "password"
    }

    response = self.client.post('/auth/signup', json=data)

    user = User.query.filter_by(email="test_user@gmail.com").first()
    
    assert response.status_code == 201        # confirms a working route #201 for new users
    assert user.username == "test_user"    # confirms a user.username as the test_user in response




  def test_user_login(self):

    data = {
      "username": "test_user",
      "password": "password"
    }

    response = self.client.post('/auth/login', json=data)
    assert response.status_code == 200        # 200 for logged in users