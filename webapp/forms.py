from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, ValidationError, SelectField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, TelField
from flask_wtf.file import FileField
import re

class Login(FlaskForm):
  username = StringField('Имя пользователя', validators=[DataRequired()])
  password = PasswordField('Пароль', render_kw = {"class": "password-field"}, validators=[DataRequired()])
  remember = BooleanField('Запомнить', default=False)
  submit = SubmitField('Войти', render_kw = {"class": "submit-button"})

class Registration(FlaskForm):
  username = StringField('Имя пользователя', validators=[DataRequired()])
  email = StringField('E-mail', render_kw = {"class": "password-username"}, validators=[DataRequired()])
  password = PasswordField('Пароль', render_kw = {"class": "password-field"})
  check_password = PasswordField('Подтвердите пароль', render_kw = {"class": "password-field"})
  submit =SubmitField('Зарегистрироваться', render_kw = {"class": "submit-button"})

class AddProduct(FlaskForm):
  product_id = HiddenField()
  product_name = HiddenField()
  product_price = HiddenField()
  product_img = HiddenField()
  submit = SubmitField('Добавить в корзину', render_kw = {"class": "submit-button"})
  

class DeleteProduct(FlaskForm):
  product_id = HiddenField()
  submit_del = SubmitField('Удалить')

class Order_form(FlaskForm):
  username = StringField('Имя получателя заказа', validators=[DataRequired()])
  phone = StringField('Телефон', validators=[DataRequired()])
  address = StringField('Адрес')
  city = StringField('Город', validators=[DataRequired()])
  street = StringField('Улица', validators=[DataRequired()])
  house = StringField('Дом/корпус', validators=[DataRequired()])
  appartement = StringField('Квартира', validators=[DataRequired()])
  date = DateField('Дата доставки', format='%Y-%m-%d')
  submit = SubmitField('Оплатить', render_kw = {"class": "submit-button"})

  def validate_phone(form, field):
    reg = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    if len(re.findall(reg, field.data)) == 0:
      raise ValidationError('Неправильный формат номер телефона')

class Cart_form(FlaskForm):
  total_price = HiddenField()
  submit_to_order = SubmitField('Оформить заказ', render_kw = {"class": "submit-button"})

class Add_merchandise(FlaskForm):
  name_merchandise = StringField('Название товара', validators=[DataRequired()])
  price_merchandise = StringField('Стоимость товара', validators=[DataRequired()])
  category_merchandise = SelectField('Категория', coerce=int,                                       choices=[
                                    (0, 'Одежда'),
                                    (1, 'Обувь'),
                                    (2, 'Сумки'),
                                    (3, 'Аксессуары'),
  ])
  quantity_merchandise = IntegerField('Количество товара на складе', validators=[DataRequired()])
  file = FileField()
  submit = SubmitField('Разместить', render_kw = {"class": "submit-button"})