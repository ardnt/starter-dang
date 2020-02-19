from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

UserModel = get_user_model()


class User(DjangoObjectType):
    class Meta:
        model = UserModel
        exclude = ('password', 'is_superuser', 'remote_id', 'is_staff')
