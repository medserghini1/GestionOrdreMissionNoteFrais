from app import db

class Mission(db.Model):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    objet = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    date_depart = db.Column(db.Date, nullable=False)
    date_retour = db.Column(db.Date, nullable=False)
    nb_nuitees = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    etat = db.Column(db.Enum('En attente', 'Validée', 'Refusée', name='etat_mission_enum'), default='En attente')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    notes_frais = db.relationship('NoteFrais', backref='mission', lazy=True)
    historiques = db.relationship('Historique', backref='mission', lazy=True)