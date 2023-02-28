from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


auth_namespace = Namespace('Auth', description='a name space for authentication')




# schema models / serializers ------------------------------------------------------------------------

SignUp_Model = auth_namespace.model( # .model('class_model name') creates schemas
  'SignUp', {
    # 'id': fields.Integer(),
    'username': fields.String(required=True, description='A username'),
    'email': fields.String(required=True, description='An email'),
    'password': fields.String(required=True, description='A Password')
  }
)

User_Model = auth_namespace.model( # for return on signup
  'User', {
    'id': fields.Integer(),
    'username': fields.String(required=True, description='A username'),
    'email': fields.String(required=True, description='An email'),
    'password_hash': fields.String(required=True, description='A Password'),
    'is_active': fields.Boolean(description='This shows if the user is active or not'),
    'is_staff': fields.Boolean(description='This shows if user is staff or not')
  }
)

Login_Model = auth_namespace.model(
  'Login', {
    'username': fields.String(required=True, description='A username'),
    'password': fields.String(required=True, description='A Password')
  }
)
# ---------------------------------------------------------------------------------------




#Resource helps combine methods to functions under the same class
# The room of inquries and orders

@auth_namespace.route('/signup')
class SignUp(Resource):

  @auth_namespace.expect(SignUp_Model) # expect from the user
  @auth_namespace.marshal_with(User_Model) # return format to the user
  def post(self):

    data = request.get_json() 

    new_user = User(
      username = data.get('username'),
      email = data.get('email'),
      password_hash = generate_password_hash(data.get('password'))

    )

    new_user.save()
    return new_user, HTTPStatus.CREATED



@auth_namespace.route('/login')
class Login(Resource):

  @auth_namespace.expect(Login_Model)
  def post(self):
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if (user is not None) and check_password_hash(user.password_hash, password):

      access_token = create_access_token(identity=user.username)
      refresh_token = create_refresh_token(identity=user.username)

      response = {
        'access_token': access_token,
        'refresh_token': refresh_token
      }

      return response, HTTPStatus.CREATED




@auth_namespace.route('/refresh') 
# this access route is used to identity the user with the refresh token and provides a new access token in return
class Refresh(Resource):
  
  @jwt_required(refresh=True)
  def post(self):

    username = get_jwt_identity()

    access_token = create_access_token(identity=username)

    return {'access_token': access_token}, HTTPStatus.OK

