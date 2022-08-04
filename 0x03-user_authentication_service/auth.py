#!/usr/bin/env python3
""" python file
    with auth class
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hash password and return
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """ generate auth """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register user """
        try:
            ouser = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pwd = _hash_password(password)
            return self._db.add_user(email, pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ check user credentials """
        try:
            user = self._db.find_user_by(email=email)
            pwd = user.hashed_password
            return bcrypt.checkpw(password.encode(), pwd)
        except NoResultFound:
            return False

    def create_session(self, email) -> str:
        """ create and return
            session
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        s_id = _generate_uuid()
        self._db.update_user(user.id, session_id=s_id)
        return s_id
