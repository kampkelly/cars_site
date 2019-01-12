import graphene
from car import Query as CarQuery, Mutation as CarMutation
from user import Query as UserQuery, Mutation as UserMutation

class Query(CarQuery, UserQuery):
    pass
class Mutation(CarMutation, UserMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
