from webapp.database import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

Product_Cart = db.Table('Product_Cart',
                        db.Column('id', db.Integer, primary_key=True),
                       db.Column('product_id', db.Integer, ForeignKey("product.id")),
                       db.Column('cart_id', db.Integer, ForeignKey("cart.id")))

#модель пользователя
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(30), unique=True)
  password = db.Column(db.Integer)
  username = db.Column(db.String(30))
  id_order = relationship("Order", lazy='dynamic', foreign_keys='[Order.user_id]')

  def __init__(self, username, email, password):
    self.email = email
    self.username = username
    self.password = password

    
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  price = db.Column(db.Integer)
  category = db.Column(db.String(30))
  quantity = db.Column(db.Integer)
  img = db.Column(db.Text)
  carts = relationship("Cart", secondary=Product_Cart, back_populates='products')

  def __init__(self, name, price, category, quantity, img):
    self.name = name
    self.price = price
    self.category = category
    self.quantity = quantity
    self.img = img

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  phone = db.Column(db.String(30))
  address = db.Column(db.String(120))
  city = db.Column(db.String(30))
  street = db.Column(db.String(40))
  house = db.Column(db.Integer)
  appartement = db.Column(db.Integer)
  user_id = db.Column(db.Integer, ForeignKey(User.id))

  def __init__(self, name, phone, address, city, street, house, appartement, user_id):
    self.name = name
    self.phone = phone
    self.address = address
    self.city = city
    self.street = street
    self.house = house
    self.appartement = appartement
    self.user_id = user_id

class Cart(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, ForeignKey(User.id))
  quantity = db.Column(db.Integer)
  products = relationship("Product", secondary=Product_Cart, back_populates='carts')

  def __init__(self, product_id, user_id, quantity):
    self.product_id = product_id
    self.user_id = user_id
    self.quantity = quantity

