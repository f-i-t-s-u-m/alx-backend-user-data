#!/usr/bin/env python3
""" flask app file
"""

from flask import Flask, jsonify, request, abort
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """ index gate """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """ create new user """
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=['POST'])
def login() -> str:
    """ generate sessions
    """
    email = request.form['email']
    paswd = request.form['password']
    chauth = AUTH.valid_login(email, paswd)

    if not chauth:
        return abort(401)

    session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    res = jsonify(msg)

    res.set_cookie("session_id", session_id)
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
