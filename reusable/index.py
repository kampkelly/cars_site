from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
import os

Session = sessionmaker()


def create_app(config_name):
    app = Flask(__name__)
    engine = None
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    if config_name == 'development':
        engine = create_engine(os.getenv('DEV_DATABASE_URL'))
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_DATABASE_URL')  # connect to database
    elif config_name == 'testing':
        engine = create_engine(os.getenv('TEST_DATABASE_URL'))
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    elif config_name == 'production':
        pass
    settings = {'app': app, 'engine': engine}
    return settings


app, engine = create_app(os.getenv('APP_SETTINGS'))['app'], create_app(os.getenv('APP_SETTINGS'))['engine']

Session.configure(bind=engine)
session = Session()

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Utility(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
