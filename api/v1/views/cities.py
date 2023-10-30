#!/usr/bin/python3
"""City views for API"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_cities(state_id):
    """Retrieves all cities of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    """Retrieves a single city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city from storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def create_city(state_id):
    """Create a city in a certain state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    """Updates a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at',
                       'updated_id']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
