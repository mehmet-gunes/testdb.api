from flask import Blueprint, jsonify, request

from repository.db import db
from repository.models import User, Tube
from repository.schemas import UserSchema, UserTubesSchema

usr = Blueprint('users', __name__)


# Get user list
@usr.route('/', methods=['GET'])
def users():
    """
    :return: List of all users
    """
    all_users = User.query.all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(all_users)
    return jsonify(result)


# Create a new user ensuring unique email
@usr.route('/', methods=['POST'])
def post_user():
    """
    Creates a new user with the email given in the request body json
    :return:
    """
    try:
        user = User.query.filter_by(email=request.json['email']).first()
        if user:
            raise ValueError()
        new_user = User(request.json['email'])
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email=request.json['email']).first()
        user_schema = UserSchema()
        return user_schema.jsonify(user)

    except AttributeError:
        return jsonify({"Error": f"User not found!"}), 400
    except ValueError:
        return jsonify({"Error": f"User {request.json['email']} already in use!"}), 400


# Delete a user's records using email
@usr.route('/<email_address>', methods=['DELETE'])
def delete_user(email_address):
    """
        Included for showing all CRUD operations but is not needed
        :param email_address:
        :return:
        """
    try:
        user = User.query.filter_by(email=email_address).first()
        Tube.query.filter_by(user_id=user.id).delete()
        User.query.filter_by(id=user.id).delete()
        db.session.commit()
        return jsonify({"Success": f"User with {email_address} deleted!"}), 200

    except AttributeError:
        return jsonify({"Error": f"User with {email_address} not found!"}), 200


# Get a user's records from email
@usr.route('/<email_address>', methods=['GET'])
def get_user(email_address):
    """
    :param email_address:
    :return: List of tubes for the user with email address given in URL
    """
    user = User.query.filter_by(email=email_address).first()
    if not user:
        return jsonify({"Error": f"User with {email_address} not found!"}), 400

    user_tubes_schema = UserTubesSchema()
    result = user_tubes_schema.dump(user)
    return jsonify(result)
