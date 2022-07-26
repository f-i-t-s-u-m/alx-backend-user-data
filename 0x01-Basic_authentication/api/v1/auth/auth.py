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
        return False

    def authorization_header(self, request=None) -> str:
        """ auth header
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user
        """
        return request
