"""
 Set currently logged in user context
"""
from graphql_jwt.utils import jwt_payload


def custom_jwt_payload_handler(user, context=None):
    payload = jwt_payload(user, context)
    payload['isMentor'] = user.is_mentor
    print("logged In User", user)
    return payload
