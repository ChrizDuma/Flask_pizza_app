import unittest
from ..utilities import db
from .. import create_app
from ..config.config import config_dict
from ..models.orders import Order
from flask_jwt_extended import create_access_token



class OrderTestCase(unittest.TestCase):
  def setUp(self):
    # 
    self.app = create_app(config_app=config_dict['test'])

    self.appctx = self.app.app_context() # creates an app context

    self.appctx.push()   # pushes created inform into the database

    self.client = self.app.test_client()

    db.create_all()       #creating tables for testing
  # 
  # 
  # 
  def tear_down(self):    # the reset before recreation
    db.drop_all()         # drops all existing tables in the db

    self.appctx.pop()     # removes an app context

    self.app = None

    self.client = None
# ----------------------------------------------------------------



  # 
  def test_create_order(self):
    
    data = {
      "size": "SMALL",
      "quantity": 1,
      "flavour": "VEGETARIAN"
    }

    token = create_access_token(identity='test_user')

    headers = {
      "Authorization": f"Bearer {token}"
    }

    response = self.client.post('/Orders/orders', headers=headers, json=data)

    orders = Order.query.all()

    # ----- checks --------
    assert response.status_code == 201
    assert len(orders) == 1       
    assert orders[0].id == 1       
    assert response.json['size'] == "Sizes.SMALL" # Sizes.___ represents the Enum class


  # 
  def test_get_all_orders(self):
    
    token = create_access_token(identity='test_user')

    headers = {
      "Authorization": f"Bearer {token}"
    }

    response = self.client.get('/Orders/orders', headers=headers)

    # ----- checks -----
    assert response.status_code == 200
    assert response.json == []  


  # 
  def test_get_single_order(self):

    token = create_access_token(identity='test_user')

    headers = {
      "Authorization": f"Bearer {token}"
    }


    order = Order(
      size = "SMALL",
      quantity = 2,
      flavour = "VEGETARIAN"
    )
    order.save()


    response = self.client.get('/Orders/order/1', headers=headers)

    assert response.status_code == 200

  

  def test_get_order_by_id(self):

    token = create_access_token(identity="test_user")

    headers = {
      "Authorization": f"Bearer {token}"
    }
    
    order = Order(
      id = 1
    )
    order.save()

    if order.id == 1:
      response = self.client.get('/Orders/order/1', headers=headers)

    
    assert response.status_code == 200

  

  def test_update_order_by_id(self):

    token = create_access_token(identity="test_user")
    headers = {
      "Authorization": f"Bearer {token}"
    }

    order = Order(
      id = 1,
      size = "SMALL",
      quantity = 2,
      flavour = "VEGETARIAN"
    )
    order.save()

    data = {
      "size": "MEDIUM",
      "quantity": 1,
      "flavour": "PEPPERONI"
    }
    order.size = data["size"]
    order.quantity = data["quantity"]
    order.flavour = data["flavour"]
    order.save()
    
    if order.id == 1:
      response = self.client.get('/Orders/order/1', headers=headers, json=data)

    assert response.status_code == 200
    assert response.json["size"] == "Sizes.MEDIUM"
    assert response.json["quantity"] == 1



  def test_delete_order_by_id(self):

    order = Order(
      id = 1
    )
    order.save()

    token = create_access_token(identity="test_user")
    headers = {
      "Authorization": f"Bearer {token}"
    }

    if order.id == 1:

      order.delete()
      response = self.client.get('/Orders/order/1', headers=headers)

    assert response.status_code == 404