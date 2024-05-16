"""Mentorship Request Schema"""

import graphene
from core.models import Request, User
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model


class RequestType(DjangoObjectType):
    """Request Model details"""

    mentor_id = graphene.Int()
    mentee_id = graphene.Int()

    class Meta:
        model = Request
        fields = ('id', 'mentor_id', 'mentee_id', 'question', 'status')

    def resolve_mentor_id(self, info):
        return self.mentor.id

    def resolve_mentee_id(self, info):
        return self.mentee.id


class CreateRequest(graphene.Mutation):
    """Create Request Mutation"""
    request = graphene.Field(RequestType)

    class Arguments:
        mentorId = graphene.Int(required=True)
        menteeId = graphene.Int(required=True)
        question = graphene.String(required=True)

    def mutate(self, info, mentorId, menteeId, question):
        User = get_user_model()
        mentor = User.objects.get(id=mentorId)
        mentee = User.objects.get(id=menteeId)
        request = Request.objects.create(
            mentor=mentor,
            mentee=mentee,
            question=question
        )
        return CreateRequest(request=request)


class AcceptRequest(graphene.Mutation):
    """Accept mentee request"""
    request = graphene.Field(RequestType)

    class Arguments:
        requestId = graphene.Int(required=True)

    def mutate(self, info, requestId):
        existing_request = Request.objects.get(id=requestId)
        existing_request.status = 'Accepted'
        existing_request.save()

        return AcceptRequest(request=existing_request)


class RejectRequest(graphene.Mutation):
    """Reject mentee request"""
    request = graphene.Field(RequestType)

    class Arguments:
        requestId = graphene.Int(required=True)

    def mutate(self, info, requestId):
        existing_request = Request.objects.get(id=requestId)
        existing_request.status = 'Rejected'
        existing_request.save()

        return RejectRequest(request=existing_request)


class RequestQueries(graphene.ObjectType):
    """Request Queries"""
    all_requests = graphene.List(RequestType)
    user_requests = graphene.List(RequestType,
                                  menteeId=graphene.Int(required=True))

    def resolve_all_requests(self, info):
        return Request.objects.all()

    def resolve_user_requests(self, info, menteeId):
        """Users can view all their mentorship sessions"""
        mentee = User.objects.get(id=menteeId)
        return Request.objects.filter(mentee=mentee)


class RequestMutations(graphene.ObjectType):
    """Request Mutations"""
    create_request = CreateRequest.Field()
    accept_request = AcceptRequest.Field()
    reject_request = RejectRequest.Field()


schema = graphene.Schema(query=RequestQueries, mutation=RequestMutations)
