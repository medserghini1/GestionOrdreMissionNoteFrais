from flask import Blueprint, request, jsonify
from app import db
from models.mission import Mission
from models.historique import Historique
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import role_required
from datetime import datetime

mission_bp = Blueprint('mission', __name__, url_prefix='/api/missions')

@mission_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('Collaborateur')
def create_mission():
    data = request.json
    user = get_jwt_identity()
    mission = Mission(
        objet=data['objet'],
        destination=data['destination'],
        date_depart=data['date_depart'],
        date_retour=data['date_retour'],
        nb_nuitees=data['nb_nuitees'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        user_id=user['id']
    )
    db.session.add(mission)
    db.session.commit()
    return jsonify({'msg': 'Ordre de mission créé'}), 201

@mission_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_mission(id):
    mission = Mission.query.get_or_404(id)
    return jsonify({
        'id': mission.id,
        'objet': mission.objet,
        'destination': mission.destination,
        'date_depart': mission.date_depart.isoformat(),
        'date_retour': mission.date_retour.isoformat(),
        'nb_nuitees': mission.nb_nuitees,
        'etat': mission.etat,
        'latitude': mission.latitude,
        'longitude': mission.longitude
    })

@mission_bp.route('/<int:id>/valider', methods=['POST'])
@jwt_required()
@role_required('Manager')
def valider_mission(id):
    mission = Mission.query.get_or_404(id)
    mission.etat = 'Validée'
    db.session.commit()
    historique = Historique(
        date=datetime.utcnow(),
        commentaire=request.json.get('commentaire', 'Mission validée'),
        etat='Validée',
        note_frais_id=None,
        validateur_id=get_jwt_identity()['id'],
        mission_id=mission.id
    )
    db.session.add(historique)
    db.session.commit()
    return jsonify({'msg': 'Ordre de mission validé.'})

@mission_bp.route('/<int:id>/refuser', methods=['POST'])
@jwt_required()
@role_required('Manager')
def refuser_mission(id):
    mission = Mission.query.get_or_404(id)
    mission.etat = 'Refusée'
    db.session.commit()
    historique = Historique(
        date=datetime.utcnow(),
        commentaire=request.json.get('commentaire', 'Mission refusée'),
        etat='Refusée',
        note_frais_id=None,
        validateur_id=get_jwt_identity()['id'],
        mission_id=mission.id
    )
    db.session.add(historique)
    db.session.commit()
    return jsonify({'msg': 'Ordre de mission refusé.'})

@mission_bp.route('/<int:id>/historique', methods=['GET'])
@jwt_required()
def historique_mission(id):
    historiques = Historique.query.filter_by(mission_id=id).all()
    return jsonify([
        {
            'date': h.date.isoformat(),
            'commentaire': h.commentaire,
            'etat': h.etat,
            'validateur_id': h.validateur_id
        } for h in historiques
    ])