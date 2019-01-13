from reusable.index import bcrypt
import jwt
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from models.user_model import UserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        only_fields = ("email", "name")


class Query(graphene.ObjectType):
    signin_user = graphene.Field(
                User,
                email=graphene.String(),
                password=graphene.String()
            )

    def resolve_signin_user(self, info, **kwargs):
        query = User.get_query(info)
        if kwargs.get('email') and kwargs.get('password'):
            find_user = query.filter(UserModel.email == kwargs.get('email')).first()
            if find_user:
                check_password = bcrypt.check_password_hash(find_user.password, kwargs.get('password'))
                if check_password:
                    # encoded_jwt = jwt.encode({'email': find_user.email, 'name': find_user.name}, 'secret', algorithm='HS256') # noqa
                    return find_user
                else:
                    raise GraphQLError('You are not authorized to login!')
            else:
                raise GraphQLError('You are not authorized to login!')
        else:
            raise GraphQLError('Bad Request!')


class SignupUser(graphene.Mutation):

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(User)
    token = graphene.String()

    def mutate(self, info, **kwargs):
        kwargs['password'] = bcrypt.generate_password_hash(kwargs['password']).decode('utf-8')
        user = UserModel(**kwargs)
        user.save()
        encoded_jwt = jwt.encode({'email': kwargs['email'], 'name': kwargs['name']}, 'secret', algorithm='HS256')
        return SignupUser(user=user, token=encoded_jwt)


class Mutation(graphene.ObjectType):
    signup_user = SignupUser.Field()
