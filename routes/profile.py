from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from app import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/api/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    return jsonify({
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "matricule": user.matricule,
        "email": user.email,
        "role": user.role,
    })

@profile_bp.route("/api/me", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    data = request.json
    # Autoriser la modification du nom et prénom seulement (jamais email/matricule/role ici)
    if "nom" in data:
        user.nom = data["nom"]
    if "prenom" in data:
        user.prenom = data["prenom"]
    if "password" in data and data["password"]:
        user.set_password(data["password"])
    db.session.commit()
    return jsonify({"message": "Profil mis à jour"})