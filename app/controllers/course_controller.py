import hashlib
from app.utils.utils import *
from app.utils.decorators import role_required
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (jwt_required)
from app.models.cource import Cource

CourseController = Blueprint('course', __name__)


@CourseController.route('/get', methods=['GET'])
@jwt_required
def get():
    return jsonify(Cource.with_('competences').get().serialize()), 200


@CourseController.route('/get/<id>', methods=['GET'])
@jwt_required
def get_course(id):
    course = Cource.with_('competences').find(id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    return jsonify(course.serialize()), 200


@CourseController.route('/create', methods=['POST'])
@jwt_required
@role_required('директор', 'методист')
def create_course():
    data = request.get_json(force=True)
    course = Cource.create(
        name=data.get('name'),
        description=data.get('description'),
        start=data.get('start')
    )
    return jsonify(course.serialize()), 200


@CourseController.route('/update/<id>', methods=['POST'])
@jwt_required
@role_required('директор', 'методист')
def update_course(id):
    data = request.get_json(force=True)
    course = Cource.where('id', id).first()
    course.name = data.get('name', '')
    course.description = data.get('description', '')
    course.start = data.get('start', '')
    course.save()
    return jsonify(course.serialize()), 200
