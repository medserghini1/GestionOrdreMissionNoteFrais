from app import db

class NoteFrais(db.Model):
    __tablename__ = 'note_frais'
    id = db.Column(db.Integer, primary_key=True)
    montant = db.Column(db.Float, nullable=False)
    type_frais = db.Column(db.Enum('Hôtel', 'Kilométrage', 'Péage', 'Repas', 'Parking', 'Train', 'Taxi', name='typefrais_enum'), nullable=False)
    justificatif = db.Column(db.String(255), nullable=True)
    etat = db.Column(db.Enum('En attente', 'Validée', 'Refusée', name='etat_frais_enum'), default='En attente')
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)

    historiques = db.relationship('Historique', backref='note_frais', lazy=True)