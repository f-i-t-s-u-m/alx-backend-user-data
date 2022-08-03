#!/usr/bin/env python3
""" user python file
    user database model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ user model """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False )
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """ return representation """
        return f"""<User(id={id}, email={email},
                    hashed_password={hashed_password},
                    session_id={session_id}, reset_token={reset_token}>"""
