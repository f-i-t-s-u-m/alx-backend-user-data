#!/usr/bin/env python3
""" basic auth python file
    with basic_auth class
"""

import base64
from api.v1.auth.auth import Auth


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
