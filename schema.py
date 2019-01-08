import graphene
from car import Query as CarQuery, Mutation as CarMutation

class Query(CarQuery):
    pass
class Mutation(CarMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
