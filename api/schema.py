import graphene

from .queries import UsersQuery


class Mutation(graphene.ObjectType):
    pass


class Query(UsersQuery):
    pass


schema = graphene.Schema(query=Query)
