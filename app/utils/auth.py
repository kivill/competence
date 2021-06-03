from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.models.user import User


class Auth:

    @staticmethod
    def unauthorized():
        return jsonify({
            'message': 'Missing Authorization Header'
        }), 401

    @staticmethod
    def refresh():
        current_user = get_jwt_identity()
        ret = {
            'token': create_access_token(identity=current_user)
        }
        return jsonify({'ok': True, 'data': ret}), 200

    @staticmethod
    def auth_user():
        user_uuid = get_jwt_identity()['token']
        return User.where('token', token).first_or_fail()

    @staticmethod
    def user():
        user_uuid = get_jwt_identity()['uuid']
        role = Auth.role()
        return User.where('uuid', user_uuid).first_or_fail()

    @staticmethod
    def role():
        identity = get_jwt_identity()
        return identity.get('role')
