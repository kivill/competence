import os
import threading
import math
from datetime import datetime
from app.utils.auth import Auth
from app.utils.utils import *
from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required, jwt_refresh_token_required)


import hashlib


from app.models.school import School

CompanyController = Blueprint('company', __name__)


@CompanyController.route('/get', methods=['GET'])
@jwt_required
def get():
    return jsonify(School.first().to_dict()), 200


@CompanyController.route('/update', methods=['POST'])
@jwt_required
def update():
    company = School.first()
    data = request.get_json(force=True)
    company.name = data.get('name', '')
    company.phone = data.get('phone', '')
    company.email = data.get('email', '')
    company.legal_address = data.get('legal_address', '')
    company.actual_address = data.get('actual_address', '')
    company.representative_name = data.get('representative_name', '')
    company.save()
    return jsonify(company.to_dict()), 200
