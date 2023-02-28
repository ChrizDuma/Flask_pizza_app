from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity


order_namespace = Namespace('Orders', description='a name space for your order')

# ------- Schema models ------------------------------

order_model = order_namespace.model(
  'Order', {
    'id': fields.Integer(description='order id'),
    'quantity': fields.Integer(required=True, description='Pizza quantity'),
    'flavour': fields.String(required=True, description='Pizza flavour', enum=['VEGETARIAN', 'PEPPERONI', 'CHICKEN', 'CHEESE', 'BEEF']),
    'size': fields.String(required=True, description='Pizza size', enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
    'order_status': fields.String(required=True, description='Order status', enum=['PENDING', 'ON_THE_WAY', 'DELIVERED'])
  }
)

order_status_model = order_namespace.model(
  'order_status',{ 
    'order_status': fields.String(required=True, description='Order status', enum=['PENDING', 'ON_THE_WAY', 'DELIVERED'])
     
  }
)
# ------------------------------------------------------------






# -------------------- Routes ------------------------

@order_namespace.route('/orders')
class Get_Create_Order(Resource):
  # ------------------------------------------
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(description="Get all orders")
  @jwt_required()
  def get(self):
    """ GET all orders """
    orders = Order.query.all()

    return orders, HTTPStatus.OK # all orders have been fetched


  # --------------------------------------- 
  @order_namespace.expect(order_model)
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(description="Post an order")
  @jwt_required()
  def post(self):
    """ POST an order """

    username = get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()

    data = order_namespace.payload # collecting data from the user

    new_order = Order(
      size = data['size'],
      quantity = data['quantity'],
      flavour = data['flavour']
    )

    new_order.user = current_user 
    new_order.save()

    return new_order, HTTPStatus.CREATED # order has been created


# -----------------------------------------------
@order_namespace.route('/order/<int:order_id>') 
class Get_Update_Delete(Resource):

  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(description="Retrieve an order by ID", params = {'order_id' : "ID for the order_to_get"})
  def get(self, order_id):
    """ Retrieve an order by id """

    order = Order.get_order_by_id(order_id)

    return order, HTTPStatus.OK
    
  # ---------------------------

  @order_namespace.expect(order_model)
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(description="Update an order by ID", params = {'order_id' : "ID for the order_to_update"})
  def put(self, order_id):
    """ update an order by id """

    order_to_update = Order.get_order_by_id(order_id)

    updates = order_namespace.payload

    order_to_update.size = updates['size']  
    order_to_update.quantity = updates['quantity']  
    order_to_update.flavour = updates['flavour']  
      
    order_to_update.save()

    return order_to_update, HTTPStatus.OK


  @order_namespace.doc(description="Delete an order", params = {'order_id' : "ID for the order_to_delete"})
  def delete(self, order_id):
    """ delete order """
    order_to_delete = Order.get_order_by_id(order_id)
    order_to_delete.delete()
    return {'message': "order deleted"}




















@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class Get_Specific_Order_by_User(Resource):

  @order_namespace.marshal_list_with(order_model)
  @order_namespace.doc(description="Get an order by User", params = {'order_id' : "ID for the order_to_get", 'user_id':"ID for current user"})
  @jwt_required()
  def get(self, user_id, order_id):
    """ Get order by user """

    user = User.get_user_by_id(user_id)

    order = Order.get_order_by_id(order_id)

    if order in user.orders:
      return order, HTTPStatus.OK
    




@order_namespace.route('/user/<int:user_id>/orders')
class User_Orders(Resource):

  @order_namespace.marshal_list_with(order_model)
  @order_namespace.doc(description="Get all orders by specific user", params = {'user_id':"ID for current user"})
  @jwt_required()
  def get(self, user_id):
    """ Get all orders for specific user """
    user = User.get_user_by_id(user_id)

    orders = user.orders
    return orders, HTTPStatus.OK



@order_namespace.route('/order/status/<int:order_id>')
class Update_Order_Status(Resource):
  
  @order_namespace.expect(order_status_model)
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(description="Update an order's status", params = {'order_id':"ID for order to update"})
  @jwt_required()
  def patch(self, order_id):
    """ update an order status """
    
    data = order_namespace.payload

    order_to_update = Order.get_order_by_id(order_id)

    order_to_update.order_status = data['order_status']

    order_to_update.save()

    return order_to_update, HTTPStatus.OK