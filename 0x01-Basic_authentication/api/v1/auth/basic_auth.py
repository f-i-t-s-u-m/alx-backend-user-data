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
        if (authorization_header is None or
           type(authorization_header) is not str):
            return None
        elif authorization_header[:6] == 'Basic ':
            return authorization_header[6:]
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
        elif User.count() < 1:
            return None
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
