from webapp import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db = SQLAlchemy(app)
# engine = create_engine('sqlite:///database.db')
# Session = sessionmaker(bind=engine)
# session = Session()