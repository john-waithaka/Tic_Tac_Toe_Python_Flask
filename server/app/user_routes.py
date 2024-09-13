# We define a Blueprint for user registration, login, and logout functionalities using sessions for session management and password hashing for security.

from flask import Blueprint, request, jsonify, session
from .models import User
from . import db
import re

user_blueprint = Blueprint('user', __name__)

def is_valid_email(email): #Checks if the provided email address follows a valid email format using a regular expression.
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# register a new user
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing fields"}), 400

    if not is_valid_email(data['email']):
        return jsonify({"message": "Invalid email format"}), 400
    # Check if a user with the same username already exists in the database
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400
    # Create a new user object with the provided username and email
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

    return jsonify({"message": "User registered successfully"}), 201

# log in a user
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = None
    # Check if a username was provided, and fetch the user by username
    if 'username' in data:
        user = User.query.filter_by(username=data['username']).first()
    if 'email' in data:
        user = User.query.filter_by(email=data['email']).first()
    #If okay then....else
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


# log out a user
@user_blueprint.route('/logout', methods=['POST'])
def logout():
    # Remove the user ID from the session to log out the user
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200
