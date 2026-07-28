   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
   app.config['TESTING'] = True
   app.secret_key = 'test-secret'
   db.init_app(app)
   with app.app_context():
       db.create_all()
   return app
   return app.test_client()
   user = User(username='testuser', password='testpass')
   db.session.add(user)
   db.session.commit()
   material = Material(name='Gold', stock_level=10)
   db.session.add(material)
   db.session.commit()
   with client.session_transaction() as sess:
       sess['user_id'] = 1  # Simulate a logged-in user
   response = client.get('/dashboard')
   assert response.status_code == 200
   assert b'Dashboard' in response.data
   response = client.get('/dashboard')
   assert response.status_code == 302  # Redirect to login
   assert b'Log In' in response.data
   with client.session_transaction() as sess:
       sess['user_id'] = 1  # Simulate a logged-in user
   response = client.post('/orders', data={'description': 'New Order'})
   assert response.status_code == 302  # Redirect after creating order
   assert Order.query.filter_by(description='New Order').first() is not None
   with client.session_transaction() as sess:
       sess['user_id'] = 1  # Simulate a logged-in user
   order = Order(description='Order to delete', user_id=1)
   db.session.add(order)
   db.session.commit()
   
   response = client.post(f'/orders/{order.id}/delete')
   assert response.status_code == 302  # Redirect after deleting order
   assert Order.query.get(order.id) is None
   response = client.post('/orders', data={'description': 'Unauthorized Order'})
   assert response.status_code == 302  # Redirect to login
   assert b'Log In' in response.data