from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

from .authentication.views import auth_namespace # routes & schemas
from .order.views import order_namespace # routes & schemas

from .models.orders import Order # db structure model
from .models.users import User # db structure model

from .config.config import config_dict 
from .utilities import db 



def create_app(config_app=config_dict['dev']):

  app = Flask(__name__)
  app.config.from_object(config_app)
  
  db.init_app(app)

  jwt = JWTManager(app)

  migrate = Migrate(app, db)

  authorizations = {
    "Bearer Auth": {
      "type": "apiKey",
      "in": "header",
      "name": "Authorization",
      "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt token to authorize ** "
    }
  }



  api = Api(app, 
            title='PizzaHut_API', 
            description='A pizza delivery REST_X API app', 
            authorizations=authorizations, 
            security= "Bearer Auth")

  api.add_namespace(order_namespace) #the path is initialized to '/'
  api.add_namespace(auth_namespace, path='/auth')

  
  # ------------ error handlers ------------------
  @api.errorhandler(NotFound)
  def not_found(error):
    return {"error": "Not Found"}, 404

  @api.errorhandler(MethodNotAllowed)
  def method_error(error):
    return {"error": "This method is not allowed"}, 404



  @app.shell_context_processor
  def make_shell_context():
    return {
      'db': db,
      'user': User,
      'order': Order
    } # when we call the flask shell in terminal

  return app