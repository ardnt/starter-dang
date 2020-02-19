import graphene

from ..types import User


class UsersQuery(graphene.ObjectType):

    current_user = graphene.Field(User)

    def resolve_current_user(self, info):
        return info.context.user
