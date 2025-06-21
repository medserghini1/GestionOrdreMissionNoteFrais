from app import db

class Historique(db.Model):
    __tablename__ = 'historique'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)
    etat = db.Column(db.String(50), nullable=False)
    note_frais_id = db.Column(db.Integer, db.ForeignKey('note_frais.id'), nullable=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=True)
    validateur_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)