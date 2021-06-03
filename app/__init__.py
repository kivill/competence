import os
import time
from flask import jsonify, send_from_directory
from app.application import FlaskApplication
from werkzeug.exceptions import HTTPException



time.tzset()
builder = FlaskApplication()
app = builder.init()


@builder.jwt.unauthorized_loader
def unauthorized(callback):
    return jsonify({'message': 'Missing Authorization Header'}), 401


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



