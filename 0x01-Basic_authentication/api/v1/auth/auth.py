#!/usr/bin/env python3
""" python file with
    auth class and functions
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """ auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require function
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ auth header
        """
        if request and request.headers.get('Authorization', None):
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user
        """
        return None
