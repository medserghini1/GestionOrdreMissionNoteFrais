from flask import Blueprint, jsonify
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'nom': u.nom, 'prenom': u.prenom, 'email': u.email, 'role': u.role} for u in users])