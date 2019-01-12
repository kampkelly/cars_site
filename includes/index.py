from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_graphql import GraphQLView
from livereload import Server, shell
import json
import jsonpickle
import jwt
from flask_bcrypt import Bcrypt
from celery import Celery

Session = sessionmaker()
engine = create_engine("postgresql://postgres:postgres@localhost/cars")
Session.configure(bind=engine)
session = Session()

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)) 
Base = declarative_base()
Base.query = db_session.query_property()

app = Flask(__name__)

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
celery = make_celery(app)
# celery.register_task('tasks.add_together')
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/cars' #connect to database
db=SQLAlchemy(app)

class Utility(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
