from webapp import app
from flask import render_template, redirect, url_for, flash, request
from webapp.forms import Login, Registration, AddProduct, DeleteProduct, Cart_form, Order_form, Add_merchandise
from webapp.models import User, db, Product, Order, Cart, Product_Cart
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.loginmanager import login_manager
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql import func
import re
from sqlalchemy.sql.expression import join, select
from werkzeug.utils import secure_filename
import os

@app.before_first_request
def create_tables():
  db.create_all()

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route("/")
def start():
  
  return render_template('start.html', Cart=Cart)

@app.route("/products", methods=['GET', 'POST'])
def products():
  form = AddProduct()
  products = Product.query.filter(Product.category == "0")
  if request.method == 'POST':
    product_id = request.form.get('product_id')
    cart_id = current_user.id
    product = Product_Cart(product_id = product_id, cart_id = cart_id)
    db.session.add(product)
    db.session.commit()
    print("Добавление успешно")
    redirect(url_for('products'))

  # count = Product.query.count()
  return render_template('products.html', form=form, Cart=Cart, products=products)


@app.route("/shoes", methods=['GET', 'POST'])
def shoes():
  form = AddProduct()
  products = Product.query.filter(Product.category == "1")
  if request.method == 'POST':
    product_id = request.form.get('product_id')
    cart_id = current_user.id
    product = Product_Cart(product_id = product_id, cart_id = cart_id)
    db.session.add(product)
    db.session.commit()
    print("Добавление успешно")
    redirect(url_for('shoes'))
  
  return render_template('shoes.html', form=form, Cart=Cart, products=products)
  

@app.route("/bags", methods=['GET', 'POST'])
def bags():
  form = AddProduct()
  products = Product.query.filter(Product.category == "2")
  if request.method == 'POST':
    product_id = request.form.get('product_id')
    cart_id = current_user.id
    product = Product_Cart(product_id = product_id, cart_id = cart_id)
    db.session.add(product)
    db.session.commit()
    print("Добавление успешно")
    redirect(url_for('bags'))
  
  return render_template('bags.html', form=form, Cart=Cart, products=products)


@app.route("/input")
def input():
  return render_template('input.html', Cart=Cart)
  

@app.route("/accessories", methods=['GET', 'POST'])
def accessories():
  form = AddProduct()
  products = Product.query.filter(Product.category == "3")
  if request.method == 'POST':
    product_id = request.form.get('product_id')
    cart_id = current_user.id
    insert_item = Product_Cart.insert().values(product_id = product_id, cart_id = cart_id)
    db.session.execute(insert_item)
    db.session.commit()
    print("Добавление успешно")
    redirect(url_for('accessories'))
  
  return render_template('accessories.html', form=form, Cart=Cart, products=products)

@app.route("/customers")
def customers():
  return render_template('customers.html', Cart=Cart)


@app.route("/partners")
def partners():
  return render_template('partners.html', Cart=Cart)


@app.route("/about-company")
def company():
  return render_template('about-company.html', Cart=Cart)


@app.route("/cart", methods=['GET', 'POST'])
def cart():
  form = DeleteProduct()
  order_form = Cart_form()
  # j = join(Product_Cart, Product,
  #         Product_Cart.c.product_id == Product.c.id)
  sel = select([Product_Cart]).select_from(j).where(Product_Cart.cart_id == current_user.id)
  product = Product_Cart.query.filter_by(user_id = current_user.id)
  if request.method == 'POST':
    if order_form.submit_to_order.data:
      return redirect(url_for('order'))
    if form.submit_del.data:
      product_id = int(request.form.get('product_id'))
      delete_product = session.query(Cart).filter(Cart.id==current_user.id).all()
      db.session.delete(delete_product)
      db.session.commit()
      return redirect(url_for('cart'))
  product = Product.query.all()
  sum_product = db.session.query(func.sum(Product.price)).scalar()
  return render_template('cart.html', form=form, sum_product=sum_product, Cart=sel, to_order=order_form, product=product)


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = Login(meta={'csrf': False})

  #проверяет, все ли поля заполнены
  print(form.validate_on_submit())
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      if check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('input'))
    return '<h1>Error</h1>'
  
  return render_template('login.html', form = form, Cart=Cart)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
  form = Registration(meta={'csrf': False})

  if form.validate_on_submit():
    username = form.username.data
    email = form.email.data
    password = form.password.data
    check_password = form.check_password.data
    
    if password != check_password:
      flash('Пароли должны совпадать')
      return redirect(url_for('registration'))
    else:
      #после получения данных из БД создаем пользователя
      hash_password = generate_password_hash(form.password.data, method='sha256')
      user = User(username=username, email=email, password=hash_password)
      try:
        db.session.add(user)
        #сохраняем данные в БД
        db.session.commit()
        return redirect(url_for('login'))
      except:
        flash('Пользователь с таким email уже существует')
        return redirect(url_for('registration'))
    
  return render_template('registr.html', form = form, Cart=Cart)


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('start'))


@app.route("/order", methods=['GET', 'POST'])
@login_required
def order():
  form = Order_form(meta={'csrf': False})
  print(form.validate_on_submit())
  print(form.errors)
  if form.validate_on_submit():
    # form.validate_phone(form.phone)
    user_id = current_user.id
    name = form.username.data
    phone = form.phone.data
    address = form.address.data
    city = form.city.data
    street = form.street.data
    house = form.house.data
    appartement = form.appartement.data
    order = Order(name, phone, address, city, street, house, appartement, user_id)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('order_done'))
  return render_template('order.html', Cart=Cart, form=form)

@app.route('/order_done')
def order_done():
  order = Order.query.filter_by(user_id=current_user.id).all()
  return render_template('order_done.html', Cart=Cart, order=order[-1])

@app.route('/add_merchandise', methods=['GET', 'POST'])
def add_merchandise():
  form = Add_merchandise(meta={'csrf': False})
  if form.validate_on_submit():
    name_merchandise = form.name_merchandise.data
    price_merchandise = form.price_merchandise.data
    category_merchandise = form.category_merchandise.data
    quantity_merchandise = form.quantity_merchandise.data
    file = form.file.data
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    add_merchandise = Product(name_merchandise, price_merchandise, category_merchandise,
                              quantity_merchandise, img=filename)
    db.session.add(add_merchandise)
    db.session.commit()
  return render_template('add_merchandise.html', Cart=Cart, form=form)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def show_product(product_id):
  product = Product.query.filter(Product.id == product_id).first()
  return render_template('product.html', Cart=Cart, product=product)

@app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
  form = Add_merchandise()
  product = db.session.query(Product).get(product_id)

  if request.method == 'POST':
    name_merchandise = form.name_merchandise.data
    price_merchandise = form.price_merchandise.data
    category_merchandise = form.category_merchandise.data
    quantity_merchandise = form.quantity_merchandise.data

    product.name = name_merchandise
    product.price = price_merchandise
    product.category = category_merchandise
    product.quantity = quantity_merchandise
    db.session.merge(product)
    db.session.commit()
    return redirect(url_for('products'))

  return render_template('edit_product.html', product=product, form=form, Cart=Cart)

@app.post("/product/<int:product_id>/delete")
def delete_product(product_id):
  product = Product.query.get(product_id)
  db.session.delete(product)
  db.session.commit()
  return redirect(url_for('products'))