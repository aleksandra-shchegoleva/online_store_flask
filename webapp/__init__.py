from flask import Flask

#инициализация и запуск проекта
app = Flask(__name__)
#обнулили пути до файлов статик
app.static_url_path = ''
app.static_folder = 'static'
app.template_folder = 'templates'
app.config['SECRET_KEY'] = 'lalallalaala'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# 'sqlite://:memory:'

from webapp import routes