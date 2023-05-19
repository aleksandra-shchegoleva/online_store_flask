from flask import Flask
import os


app = Flask(__name__)

app.static_url_path = ''
app.static_folder = 'static'
app.template_folder = 'templates'
app.config['SECRET_KEY'] = 'lalallalaala'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# 'sqlite://:memory:'

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'static/images')
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from webapp import routes