#!/usr/bin/python3
"""Places model view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns a list of place objects belonging to a city"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        place = [place.to_dict() for place in city.places]
        return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Returns a place object identified by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}, 400)

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}, 400)

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        return jsonify({"error": "Missing name"}, 400)

    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    return jsonify(new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}, 400)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
