from app.utils.utils import *
from app.utils.decorators import role_required
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (jwt_required)


import hashlib


from app.models.school import School

SchoolController = Blueprint('school', __name__)


@SchoolController.route('/get', methods=['GET'])
@jwt_required
def get():
    return jsonify(School.first().to_dict()), 200


@SchoolController.route('/update', methods=['POST'])
@jwt_required
@role_required('директор')
def update():
    school = School.first()
    data = request.get_json(force=True)
    school.name = data.get('name', '')
    school.address = data.get('address', '')
    school.save()
    return jsonify(school.to_dict()), 200
