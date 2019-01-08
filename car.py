from includes.index import *

class CarModel(Base, Utility):
    __tablename__="cars"
    id=Column(Integer, primary_key=True)
    colour=Column(String(100), default='black')
    model=Column(String(100), nullable=False)
    name=Column(String(120), nullable=False, unique=True)
    year=Column(Integer, nullable=False)

class Car(SQLAlchemyObjectType):
    class Meta:
        model = CarModel
        only_fields = ("colour","model","name","year")

class Query(graphene.ObjectType):
    cars = graphene.List(
        Car,
        name=graphene.String()
        )
    view_car = graphene.Field(
        Car, 
        name=graphene.String()
        )

    def resolve_cars(self, info, **kwargs):
        query = Car.get_query(info)
        if kwargs.get('name'):
            return query.filter(CarModel.name.ilike("%" + kwargs.get('name') + "%")).all()
        else:
            return query.all()
    
    def resolve_view_car(self, info, **kwargs):
        query = Car.get_query(info)
        return query.filter(CarModel.name.ilike("%" + kwargs.get('name') + "%")).first()

class CreateCar(graphene.Mutation):

    class Arguments:
        colour = graphene.String()
        model = graphene.String(required=True)
        name = graphene.String(required=True)
        year = graphene.Int(required=True)
    car = graphene.Field(Car)

    def mutate(self, info, **kwargs):
        car = CarModel(**kwargs)
        car.save()
        return CreateCar(car=car)

class Mutation(graphene.ObjectType):
    create_car = CreateCar.Field()
