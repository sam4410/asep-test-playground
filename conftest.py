    with application.app_context():
        from extensions import db
        db.create_all()
        yield application
        db.drop_all()

@pytest.fixture()
