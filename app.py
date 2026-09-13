import os
import secrets

from flask import Flask, jsonify, render_template
from models import db
from routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config.setdefault('SECRET_KEY', os.environ.get('SECRET_KEY', secrets.token_hex(32)))
    app.config.setdefault('AUTH_TOKEN_TTL_SECONDS', 3600)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/signup")
    def signup_page():
        return render_template("signup.html")

    @app.route("/dashboard")
    def dashboard_page():
        # Authentication is intentionally handled by the client with its
        # persisted bearer token and by the protected API endpoints.
        return render_template("dashboard.html")

    register_routes(app)
    return app

if __name__ == "__main__":
    create_app().run(debug=False)
app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=False)
