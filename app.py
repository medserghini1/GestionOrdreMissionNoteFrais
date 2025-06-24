from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config

db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from models import user, mission, note_frais, historique
    from routes.auth import auth_bp
    from routes.mission import mission_bp
    from routes.note_frais import note_frais_bp
    from routes.user import user_bp
    from routes.upload import upload_bp
    from routes.profile import profile_bp  # <-- Ajout de l'import ici

    app.register_blueprint(auth_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(note_frais_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(profile_bp)  # <-- Enregistrement du blueprint profil

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)