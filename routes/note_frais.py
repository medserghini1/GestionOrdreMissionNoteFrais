from flask import Blueprint, request, jsonify
from app import db
from models.note_frais import NoteFrais
from models.historique import Historique
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import role_required
from datetime import datetime

note_frais_bp = Blueprint('note_frais', __name__, url_prefix='/api/notesfrais')

@note_frais_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('Collaborateur')
def create_note_frais():
    data = request.json
    note = NoteFrais(
        montant=data['montant'],
        type_frais=data['type_frais'],
        justificatif=data.get('justificatif'),
        mission_id=data['mission_id']
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({'msg': 'Note de frais créée'}), 201

@note_frais_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_note_frais(id):
    note = NoteFrais.query.get_or_404(id)
    return jsonify({
        'id': note.id,
        'montant': note.montant,
        'type_frais': note.type_frais,
        'justificatif': note.justificatif,
        'etat': note.etat
    })

@note_frais_bp.route('/<int:id>/valider', methods=['POST'])
@jwt_required()
@role_required('Manager', 'RH')
def valider_note_frais(id):
    note = NoteFrais.query.get_or_404(id)
    note.etat = 'Validée'
    db.session.commit()
    historique = Historique(
        date=datetime.utcnow(),
        commentaire=request.json.get('commentaire', 'Note de frais validée'),
        etat='Validée',
        note_frais_id=note.id,
        validateur_id=get_jwt_identity()['id'],
        mission_id=None
    )
    db.session.add(historique)
    db.session.commit()
    return jsonify({'msg': 'Note de frais validée.'})

@note_frais_bp.route('/<int:id>/refuser', methods=['POST'])
@jwt_required()
@role_required('Manager', 'RH')
def refuser_note_frais(id):
    note = NoteFrais.query.get_or_404(id)
    note.etat = 'Refusée'
    db.session.commit()
    historique = Historique(
        date=datetime.utcnow(),
        commentaire=request.json.get('commentaire', 'Note de frais refusée'),
        etat='Refusée',
        note_frais_id=note.id,
        validateur_id=get_jwt_identity()['id'],
        mission_id=None
    )
    db.session.add(historique)
    db.session.commit()
    return jsonify({'msg': 'Note de frais refusée.'})

@note_frais_bp.route('/<int:id>/historique', methods=['GET'])
@jwt_required()
def historique_note_frais(id):
    historiques = Historique.query.filter_by(note_frais_id=id).all()
    return jsonify([
        {
            'date': h.date.isoformat(),
            'commentaire': h.commentaire,
            'etat': h.etat,
            'validateur_id': h.validateur_id
        } for h in historiques
    ])