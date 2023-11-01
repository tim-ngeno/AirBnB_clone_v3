#!/usr/bin/python3
"""Model view for Users"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get a list of all User objects"""
    users = storage.all(User)
    u = [user.to_dict() for user in users.values()]
    return jsonify(u)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_with_id(user_id):
    """Return a user with the specified ID"""
    if user_id:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        else:
            return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Remove a user object from storage"""
    if user_id:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        else:
            storage.delete(user)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}),
                             400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}),
                             400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates user information"""
    if user_id:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}),
                                 400)
        for key, value in request.get_json().items():
            if key not in ['id', 'email', 'created_at',
                           'updated_at']:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
