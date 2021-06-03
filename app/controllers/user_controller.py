import os
import threading
import math
import uuid
from datetime import datetime
from app.utils.auth import Auth
from app.utils.utils import *
from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required, jwt_refresh_token_required, decode_token)


import hashlib


from app.models.user import User

UserController = Blueprint('user', __name__)


@UserController.route('/login', methods=['POST'])
def auth():
    data = request.get_json(force=True)
    user = User.where('email', str(data.get('email'))).first()
    if not user:
        return '', 400

    if not (user.password == str(data.get('password'))):
        return '', 400

    access_token = create_access_token(identity=user.get_jwt_identity())
    refresh_token = create_refresh_token(identity=user.get_jwt_identity())

    user.token = access_token
    user.refresh_token = refresh_token
    user.save()

    return jsonify(user.to_dict()), 200


@UserController.route('/loginbytoken', methods=['POST'])
def auth_by_token():
    data = request.get_json(force=True)
    token = data.get('token')
    decoded_token = decode_token(token)
    current_user = decoded_token['identity']
    user = User.where('uuid', current_user['uuid']).first()
    if not user:
        return '', 400

    # access_token = create_access_token(identity=user.get_jwt_identity())
    # refresh_token = create_refresh_token(identity=user.get_jwt_identity())

    # user.token = access_token
    # user.refresh_token = refresh_token
    user.save()

    return jsonify(user.to_dict()), 200


@UserController.route('/authuser', methods=['GET'])
@jwt_required
def auth_user():
    return jsonify(Auth.auth_user().serialize()), 200


@UserController.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@UserController.route('/logout', methods=['POST'])
@jwt_required
def logout():
    return '', 200


@UserController.route('/get', methods=['GET'])
@jwt_required
def get_users():
    return jsonify(User.order_by('id', 'asc').get().serialize()), 200


@UserController.route('/get/<id>', methods=['GET'])
@jwt_required
def get_user(id):
    return jsonify(User.where('id', id).first().serialize()), 200


@UserController.route('/update/<id>', methods=['POST'])
@jwt_required
def update_user(id):
    data = request.get_json(force=True)
    user = User.where('id', id).first()
    user.password = data.get('password')
    user.salary = data.get('salary')
    user.phone = data.get('phone')
    user.position = data.get('position')
    user.save()
    return jsonify(User.where('id', id).first().serialize()), 200


@UserController.route('/create', methods=['POST'])
@jwt_required
def create_user():
    data = request.get_json(force=True)
    user = User.create(
        company_id=1,
        username=data.get('full_name'),
        full_name=data.get('full_name'),
        email=data.get('email'),
        salary=data.get('salary'),
        phone=data.get('phone'),
        birthday=datetime.now(),
        start_work=datetime.now(),
        sex=data.get('sex'),
        position=data.get('position'),
        password=data.get('password'),
        uuid=str(uuid.uuid4())
    )
    return '', 200
