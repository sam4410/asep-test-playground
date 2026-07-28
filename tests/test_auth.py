   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
   app.config['TESTING'] = True
   app.secret_key = 'test-secret'
   db.init_app(app)
   with app.app_context():
       db.create_all()
   yield app
   return app.test_client()
   user = User(username='testuser', password='testpass')
   db.session.add(user)
   db.session.commit()
   response = client.post('/signup', data={'username': 'newuser', 'password': 'newpass'})
   assert response.status_code == 302  # Redirect after signup
   assert User.query.filter_by(username='newuser').first() is not None
   response = client.post('/signup', data={'username': 'testuser', 'password': 'newpass'})
   assert response.status_code == 302  # Redirect after error
   assert b'Username already exists.' in response.data
   response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
   assert response.status_code == 302  # Redirect after login
   with client.session_transaction() as sess:
       assert 'user_id' in sess
   response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpass'})
   assert response.status_code == 302  # Redirect after error
   assert b'Invalid username or password.' in response.data
   with client.session_transaction() as sess:
       sess['user_id'] = 1  # Simulate a logged-in user
   response = client.get('/logout')
   assert response.status_code == 302  # Redirect after logout
   with client.session_transaction() as sess:
       assert 'user_id' not in sess
       assert b'You have been logged out.' in response.data