import uuid
from app.utils.auth import Auth
from app.utils.utils import *
from app.utils.decorators import role_required
from flask import Blueprint, request, jsonify
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
@role_required('директор', 'методист')
def get_users():
    return jsonify(User.order_by('id', 'asc').get().serialize()), 200


@UserController.route('/get/<id>', methods=['GET'])
@jwt_required
def get_user(id):
    return jsonify(User.where('id', id).first().serialize()), 200


@UserController.route('/update/<id>', methods=['POST'])
@jwt_required
@role_required('директор', 'методист')
def update_user(id):
    data = request.get_json(force=True)
    user = User.where('id', id).first()
    user.password = data.get('password')
    user.save()
    return jsonify(user.serialize()), 200


@UserController.route('/create', methods=['POST'])
@jwt_required
@role_required('директор')
def create_user():
    data = request.get_json(force=True)
    user = User.create(
        school_id=1,
        full_name=data.get('full_name'),
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('position'),
        uuid=str(uuid.uuid4())
    )
    return user, 200
