import hashlib
from app.utils.utils import *
from app.utils.decorators import role_required
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (jwt_required)
from app.models.competence import Competence

CompetenceController = Blueprint('competence', __name__)


@CompetenceController.route('/get', methods=['GET'])
@jwt_required
def get():
    return jsonify(Competence.get().serialize()), 200


@CompetenceController.route('/get/<id>', methods=['GET'])
@jwt_required
def get_competence(id):
    competence = Competence.find(id)
    if not competence:
        return jsonify({'message': 'Competence not found'}), 404
    return jsonify(competence.serialize()), 200


@CompetenceController.route('/create', methods=['POST'])
@jwt_required
@role_required('директор', 'методист')
def create_competence():
    data = request.get_json(force=True)
    competence = Competence.create(
        name=data.get('name'),
        description=data.get('description'),
    )
    return jsonify(competence.serialize()), 200


@CompetenceController.route('/update/<id>', methods=['POST'])
@jwt_required
@role_required('директор', 'методист')
def update_competence(id):
    data = request.get_json(force=True)
    competence = Competence.where('id', id).first()
    if not competence:
        return jsonify({'message': 'Competence not found'}), 404
    competence.name = data.get('name', '')
    competence.description = data.get('description', '')
    competence.save()
    return jsonify(competence.serialize()), 200
