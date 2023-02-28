from ..utilities import db
from enum import Enum
from datetime import datetime


# ENUMs for import into the Order class
# -------------------------------------
class Sizes(Enum):
  SMALL = 'small'
  MEDIUM = 'medium'
  LARGE = 'large'
  EXTRA_LARGE = 'extra_large'

class Flavour(Enum):
  VEGETARIAN = 'vegetarian'
  PEPPERONI = 'pepperoni'
  CHICKEN = 'chicken'
  CHEESE = 'cheese'
  BEEF = 'beef'

class Status(Enum):
  PENDING = 'pending'
  ON_THE_WAY = 'on its way'
  DELIVERED = 'delivered'




class Order(db.Model):
  __tablename__='orders'
  id = db.Column(db.Integer(), primary_key=True)
  quantity = db.Column(db.Integer())
  size = db.Column(db.Enum(Sizes), default=Sizes.MEDIUM)
  flavour = db.Column(db.Enum(Flavour), nullable=False, default=Flavour.BEEF)
  order_status = db.Column(db.Enum(Status), default=Status.PENDING)
  order_date = db.Column(db.DateTime(), default= datetime.utcnow)
  customer = db.Column(db.Integer(), db.ForeignKey('users.id'))


  # ------- class functions ----------

  def __repr__(self):
    return f'<Order {self.id}>'

  def save(self):
    db.session.add(self)
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def get_order_by_id(cls, id):
    return cls.query.get_or_404(id)

  