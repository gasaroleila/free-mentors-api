"""
Tests for Request API
"""

from django.test import TestCase
from graphene.test import Client
from request.schema import schema
from core.models import Request
from django.contrib.auth import get_user_model


class RequestTestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)
        User = get_user_model()
        self.mentor = User.objects.create_user(
            first_name='mentor',
            email='mentor@example.com',
            password='mentor')
        self.mentee = User.objects.create_user(
            first_name='mentee',
            email='mentee@example.com',
            password='mentee')
        self.mentee2 = User.objects.create_user(
            first_name='mentee2',
            email='mentee2@example.com',
            password='mentee2')
        self.request1 = Request.objects.create(
            mentor=self.mentor,
            mentee=self.mentee,
            question='Test question 1',
            status='Pending')
        self.request2 = Request.objects.create(
            mentor=self.mentor,
            mentee=self.mentee2,
            question='Test question 2',
            status='Accepted')

    # def test_create_request_mutation(self):
    #     """Test create a mentorship request"""
    #     mutation = '''
    #     mutation {
    #         createRequest
    #         (mentorId: %d,
    #         question: "Test question"
    #         ) {
    #             request {
    #                 id
    #                 mentorId
    #                 menteeId
    #                 question
    #                 status
    #             }
    #         }
    #     }
    #     ''' % (self.mentor.id)

    #     executed = self.client.execute(mutation)

    #     expected_data = {
    #         'createRequest': {
    #             'request': {
    #                 'id': '3',
    #                 'mentorId': self.mentor.id,
    #                 'menteeId': self.mentee.id,
    #                 'question': 'Test question',
    #                 'status': 'Pending'
    #             }
    #         }
    #     }

    #     # Check that there are no errors
    #     # assert 'errors' not in executed

    #     # Check the response
    #     self.assertDictEqual(executed['data'], expected_data)

    def test_accept_request(self):
        """Test accept mentorship request"""
        acceptMutation = """
           mutation {
               acceptRequest(requestId: 1) {
                   request {
                    id
                    mentorId
                    menteeId
                    question
                    status
                }
               }
           }
        """

        executed = self.client.execute(acceptMutation)

        expected_data = {
            'acceptRequest': {
                'request': {
                    'id': '1',
                    'mentorId': 1,
                    'menteeId': 2,
                    'question': 'Test question 1',
                    'status': 'Accepted'
                }
            }
        }

        # Check that there are no errors
        assert 'errors' not in executed

        # Check the response
        self.assertDictEqual(executed['data'], expected_data)

    def test_reject_request(self):
        """Test reject mentorship request"""

        acceptMutation = """
           mutation {
               rejectRequest(requestId: 2) {
                   request {
                    id
                    mentorId
                    menteeId
                    question
                    status
                }
               }
           }
        """

        executed = self.client.execute(acceptMutation)

        expected_data = {
            'rejectRequest': {
                'request': {
                    'id': '2',
                    'mentorId': 1,
                    'menteeId': 3,
                    'question': 'Test question 2',
                    'status': 'Rejected'
                }
            }
        }

        # Check that there are no errors
        assert 'errors' not in executed

        # Check the response
        self.assertDictEqual(executed['data'], expected_data)

    def test_resolve_user_requests(self):
        """Test resolving user requests"""
        mentee_id = self.mentee.id

        query = '''
            query UserRequests($menteeId: Int!) {
                userRequests(menteeId: $menteeId) {
                    id
                    mentorId
                    menteeId
                    question
                    status
                }
            }
         '''

        variables = {
            'menteeId': mentee_id,  # Pass the correct variable name
        }

        expected_data = {
            'userRequests': [{
                'id': str(self.request1.id),
                'mentorId': self.mentor.id,
                'menteeId': self.mentee.id,
                'question': 'Test question 1',
                'status': 'Pending'
            }]
        }

        # Execute the query
        executed = self.client.execute(query, variables=variables)

        # Check that there are no errors
        assert 'errors' not in executed

        # Check the response
        self.assertDictEqual(executed['data'], expected_data)
