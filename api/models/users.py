from ..utilities import db

class User(db.Model):
  __tablename__='users'
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(55), nullable=False, unique=True)
  email = db.Column(db.String(55), nullable=False, unique=True)
  password_hash = db.Column(db.String(), nullable=False)
  is_staff = db.Column(db.Boolean(), default=False)
  is_active = db.Column(db.Boolean(), default=False) 
  orders = db.relationship('Order', backref='user', lazy=True)

  def __repr__(self):
    return f'<user {User.username}>'

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def get_user_by_id(cls, id):
    return cls.query.get_or_404(id)

# we can edit our database stracture here in the models directory...but the access to the db to impliment these changes, can only be granted from the utilities directory, we can use this Access when and if its granted to create sessions of access, to add structural models to the database, to store visitors information etc...