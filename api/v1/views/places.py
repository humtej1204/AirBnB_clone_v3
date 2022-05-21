#!/usr/bin/python3
'''
Create a new view for Place objects that handles
all default RESTFul API actions
'''
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_place_method(city_id):
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.place])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_method(place_id):
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place_method(place_id):
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_city_method(city_id):
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, {'message': 'Not a JSON'})
    if 'user_id' not in res:
        abort(400, {'message': 'Missing user_id'})
    user = storage.get(User, res['user_id'])
    if user is None:
        abort(404)
    if 'name' not in res:
        abort(400, {'message': 'Missing name'})
    new_place = Place(**res)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city_method(city_id):
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
