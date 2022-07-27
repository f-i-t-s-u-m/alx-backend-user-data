#!/usr/bin/env python3
""" basic auth python file
    with basic_auth class
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ basic auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base64 auth header
        """
        if (authorization_header is None or
           type(authorization_header) is not str):
            return None
        elif authorization_header[:6] == 'Basic ':
            return authorization_header[6:]
        return None
