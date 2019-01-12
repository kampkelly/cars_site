from includes.index import *

class UserModel(Base, Utility):
    __tablename__ ="users"
    id=Column(Integer, primary_key=True)
    email=Column(String(100), nullable=False, unique=True)
    name=Column(String(255), nullable=False, unique=True)
    password=Column(String(255), nullable=False)

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        only_fields = ("email", "name")

class SignupUser(graphene.Mutation):

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(User)
    token = graphene.String()

    def mutate(self, info, **kwargs):
        kwargs['password'] = bcrypt.generate_password_hash(kwargs['password'])
        user = UserModel(**kwargs)
        user.save()
        encoded_jwt = jwt.encode({'email': kwargs['email'], 'name': kwargs['name']}, 'secret', algorithm='HS256')
        return SignupUser(user=user, token=encoded_jwt)

class Mutation(graphene.ObjectType):
    signup_user = SignupUser.Field()
