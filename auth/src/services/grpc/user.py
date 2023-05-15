from flask_jwt_extended import decode_token

from core.grpc.user_pb2 import UserResponse, UserTokenRequest
from core.grpc.user_pb2_grpc import DetailerServicer


class UserFetcher(DetailerServicer):
    """Class to fetch user dat by grpc."""

    def GetUserRole(self, request: UserTokenRequest) -> UserResponse:  # noqa
        user = decode_token(request.token).get('identity')

        return UserResponse(id=user.get('id'), role=user.get('role'))
