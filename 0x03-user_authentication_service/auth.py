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

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """It takes a single session_id string argument
        Returns a string or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session ID to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token if user exists"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Uses reset token to validate update of users password"""
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
