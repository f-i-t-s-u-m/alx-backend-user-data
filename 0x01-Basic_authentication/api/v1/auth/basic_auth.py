#!/usr/bin/env python3
""" basic auth python file
    with basic_auth class
"""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ basic auth class
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """ extract base64 auth header
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """ decode base64 auth
        """
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            return f"""{base64.b64decode(base64_authorization_header)
                       .decode('utf-8')}"""
        except Exception as e:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ exract and return user info
        """
        dbah = decoded_base64_authorization_header
        if dbah is None or type(dbah) is not str:
            return (None, None)
        if len(dbah.split(':')) <= 1:
            return (None, None)

        return (dbah.split(':')[0], dbah.split(':')[1])

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ user object from
            credentials
        """
        if user_email is None or type(user_email) is not str:
            return None
        elif user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)

        if not auth_header:
            return None

        encoded = self.extract_base64_authorization_header(auth_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)

        if not email or not pwd:
            return None

        user = self.user_object_from_credentials(email, pwd)

        return user
