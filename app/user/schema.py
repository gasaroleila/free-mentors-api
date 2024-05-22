"""
User Graphql schema
"""

import graphene
from graphene_django.types import DjangoObjectType
from core.models import User
from graphql_jwt.shortcuts import get_token
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_auth.schema import UserQuery, MeQuery
from graphql_jwt.exceptions import JSONWebTokenError
from django.contrib.auth import authenticate
from graphql_jwt import ObtainJSONWebToken


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'address',
                  'bio', 'occupation', 'expertise',
                  'is_active', 'is_mentor', 'is_staff')


class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refreshToken = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        address = graphene.String()
        bio = graphene.String()
        occupation = graphene.String()
        expertise = graphene.String()
        is_active = graphene.Boolean()
        is_mentor = graphene.Boolean()
        is_staff = graphene.Boolean()

    def mutate(self, info, email, password, **kwargs):
        user = User.objects.create_user(
            email=email,
            password=password,
            **kwargs
        )
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        return RegisterUser(user=user, token=token, refreshToken=refresh_token)


class LoginUser(graphene.Mutation):
    token = graphene.String()
    refreshToken = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = authenticate(
            username=email,
            password=password,
        )

        if user is None:
            raise JSONWebTokenError("Invalid credentials")

        token = get_token(user)
        refresh_token = create_refresh_token(user)
        return LoginUser(token=token, refreshToken=refresh_token)


class AuthMutation(graphene.ObjectType):
    """Auth Mutation"""
    register_user = RegisterUser.Field()
    token_auth = ObtainJSONWebToken.Field()


class ChangeUserToMentor(graphene.Mutation):
    """Change User To Mentor Mutation"""
    success = graphene.Boolean()

    def mutate(root, info, **kwargs):
        try:
            print("info", info.context.user)
            user = info.context.user
            user.is_mentor = True
            user.save()
            success = True
        except User.DoesNotExist:
            success = False

        return ChangeUserToMentor(success=success)


class Query(UserQuery, MeQuery, graphene.ObjectType):
    """User Query"""
    users = graphene.List(UserType)
    mentors = graphene.List(UserType)
    mentor = graphene.Field(UserType, mentor_id=graphene.Int(required=True))

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_mentors(self, info, **kwargs):
        return User.objects.filter(is_mentor=True)

    def resolve_mentor(self, info, mentor_id):
        return User.objects.get(id=mentor_id, is_mentor=True)


class Mutation(AuthMutation, graphene.ObjectType):
    """User Mutation"""
    change_user_to_mentor = ChangeUserToMentor.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
