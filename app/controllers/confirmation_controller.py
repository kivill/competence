import hashlib
import os
import uuid
from app.utils.utils import *
from app.utils.decorators import role_required
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.models.confirmation import Confirmation
from app.models.confirmation_file import ConfirmationFile

ConfirmationController = Blueprint('confirmation', __name__)


@ConfirmationController.route('/get', methods=['GET'])
@jwt_required
def get():
    user = get_jwt_identity()
    if user['role'] in ['учитель']:
        return jsonify(Confirmation.where('user_id', user['id']).get().serialize()), 200
    return jsonify(Confirmation.get().serialize()), 200


@ConfirmationController.route('/get/<id>', methods=['GET'])
@jwt_required
def get_confirmation(id):
    confirmation = Confirmation.find(id)
    if not confirmation:
        return jsonify({'message': 'Confirmation not found'}), 404
    return jsonify(confirmation.serialize()), 200


@ConfirmationController.route('/create', methods=['POST'])
@jwt_required
def create_confirmation():
    confirmation = Confirmation.create(
        user_id=request.form.get('user_id'),
        competence_id=request.form.get('competence_id'),
        status=request.form.get('status', 'processing'),
    )
    for file in request.files:
        add_img = request.files.get(file)
        filename = str(uuid.uuid4()) + '.' + add_img.filename.rsplit('.', 1)[1]
        add_img.save(os.path.join('./confirmation_files', filename))
        ConfirmationFile.create(
            confirmation_id=confirmation.id,
            file_url='http://localhost:5000/confirmation_files/'+filename
        )
    return jsonify(confirmation.serialize()), 200


@ConfirmationController.route('/update/<id>', methods=['POST'])
@jwt_required
def update_confirmation(id):
    data = request.get_json(force=True)
    confirmation = Confirmation.where('id', id).first()
    if not confirmation:
        return jsonify({'message': 'Confirmation not found'}), 404
    confirmation.status = data.get('status')
    confirmation.save()
    return jsonify(confirmation.serialize()), 200
