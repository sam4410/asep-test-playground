import os
from flask import Flask, session
from extensions import db

def create_app():
    app = Flask(__name__)    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.feature import feature_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(feature_bp)
    with app.app_context():
        db.create_all()
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)