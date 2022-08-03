#!/usr/bin/env python3
""" python file
    with auth class
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ hash password and return
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
