import pytest
import sys
sys.path.insert(0, '')  # Ensure the root directory is in the path

from app import create_app

@pytest.fixture(scope='session')
def app():
    application = create_app()
    application.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret',
    })
    with application.app_context():
        from extensions import db
        db.create_all()
        yield application
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()