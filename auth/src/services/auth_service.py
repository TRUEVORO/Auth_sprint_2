import requests
from flask import Response, jsonify, redirect, request, session, url_for
from flask_jwt_extended import get_jwt_identity
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

from models import AuthHistoryOrm, LoginRequest, RoleOrm, SignupRequest, User, UserOrm

from .base_service import BaseService
from .utils import define_device, error_handler


class AuthenticationService(BaseService):
    """Authentication service."""

    @error_handler()
    def google_auth(self) -> Response:
        """Google auth method."""

        flow = Flow.from_client_secrets_file(
            client_secrets_file=self.settings.client_secrets_file,
            scopes=self.settings.scopes,
            redirect_uri=url_for('auth.google_callback', _external=True),
        )

        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        session['state'] = state

        return redirect(authorization_url)

    @error_handler()
    def google_callback(self):
        """Google callback method."""

        state = session['state']

        flow = Flow.from_client_secrets_file(
            client_secrets_file=self.settings.client_secrets_file,
            scopes=self.settings.scopes,
            state=state,
            redirect_uri=url_for('auth.google_callback', _external=True),
        )

        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        request_session = requests.session()
        token_request = GoogleRequest(session=request_session)

        id_info = id_token.verify_oauth2_token(id_token=credentials._id_token, request=token_request)  # noqa
        session['google_id'] = id_info.get('sub')
        email = id_info.get('email')

        user = User.from_orm(self.client.retrieve(UserOrm, email=email))
        user_agent = request.headers.get('User-Agent')

        if not user:
            return self.sign_up({'email': email})

        self.client.create(
            AuthHistoryOrm, user_id=user.id, user_agent=user_agent, user_device_type=define_device(user_agent)
        )

        return jsonify(self._create_tokens(user.id, user.get_roles(), is_fresh=True))

    @error_handler()
    def sign_up(self, request_data: dict) -> Response:
        """Sign up method."""

        user = SignupRequest(**request_data).user
        base_role = self.client.retrieve(RoleOrm, name='user')

        user_agent = request.headers.get('User-Agent')

        self.client.create(UserOrm, **user.dict(exclude={'auth_history', 'roles'}), roles=[base_role])
        self.client.create(
            AuthHistoryOrm, user_id=user.id, user_agent=user_agent, user_device_type=define_device(user_agent)
        )

        return jsonify(self._create_tokens(user.id, [base_role.name], is_fresh=True))

    @error_handler()
    def sign_in(self, request_data: dict) -> Response:
        """Sign in method."""

        user = LoginRequest(**request_data).user

        user_agent = request.headers.get('User-Agent')

        self.client.create(
            AuthHistoryOrm, user_id=user.id, user_agent=user_agent, user_device_type=define_device(user_agent)
        )

        return jsonify(self._create_tokens(user.id, user.get_roles(), is_fresh=True))

    @error_handler()
    def refresh(self) -> Response:
        """Refresh method."""

        user = get_jwt_identity()

        self._revoke_tokens()

        return jsonify(self._create_tokens(user.get('user_id'), user.get('user_roles')))

    @error_handler()
    def sign_out(self) -> Response:
        """Sign out method."""

        self._revoke_tokens()
        return jsonify('signed out')

    @error_handler()
    def auth_history(self) -> Response:
        """Sign out method."""

        user = get_jwt_identity()

        auth_history = User.from_orm(self.client.retrieve(UserOrm, id=user.get('user_id'))).auth_history
        return jsonify([auth.dict(include={'user_agent', 'timestamp'}) for auth in auth_history][::-1][:10])
