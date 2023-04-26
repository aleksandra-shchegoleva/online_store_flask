from webapp import app
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
#какая функция отвечает за вывод формы авторизации
login_manager.login_view = 'login'