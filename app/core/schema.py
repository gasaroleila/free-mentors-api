# core/schema.py (or any common location in your project)
import graphene
from user.schema import Query as UserQuery, Mutation as UserMutation
from request.schema import (
    RequestQueries as RequestQuery,
    RequestMutations as RequestMutation
)


class Query(UserQuery, RequestQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, RequestMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
