import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/justificatif', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'msg': 'Aucun fichier envoyé'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return jsonify({'filename': filename}), 201
    return jsonify({'msg': 'Type de fichier non autorisé'}), 400