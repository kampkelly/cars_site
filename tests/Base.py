from schema import schema
from reusable.index import app, bcrypt, Base, engine, db_session
from models.car_model import CarModel
from models.user_model import UserModel
from flask_testing import TestCase
from graphene.test import Client

# sys.path.append(os.getcwd())


class BaseTestCase(TestCase):

    def create_app(self):
        self.base_url = 'https://127.0.0.1:3000/cars'
        self.headers = {'content-type': 'application/json'}
        self.client = Client(schema)
        return app

    def setUp(self):
        app = self.create_app()
        self.app_test = app.test_client()
        with app.app_context():
            Base.metadata.create_all(bind=engine)
            password = bcrypt.generate_password_hash('password').decode('utf-8')
            user = UserModel(email="kamp@example.com", name="Kamp", password=password)
            user.save()
            cars = CarModel(colour="black", model="BMW", name="BMW", year=2017)
            cars.save()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            db_session.remove()
            Base.metadata.drop_all(bind=engine)
