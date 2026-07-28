   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       if User.query.filter_by(username=username).first():
           flash('Username already exists.')
           return redirect(url_for('auth.signup'))
       hashed_password = generate_password_hash(password, method='sha256')
       new_user = User(username=username, password=hashed_password)
       db.session.add(new_user)
       db.session.commit()
       flash('Sign up successful! You can now log in.')
       return redirect(url_for('auth.login'))
   return '''
       <form method="post">
           <label for="username">Username:</label>
           <input type="text" name="username" required>
           <label for="password">Password:</label>
           <input type="password" name="password" required>
           <input type="submit" value="Sign Up">
       </form>
   '''
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       user = User.query.filter_by(username=username).first()
       if user and check_password_hash(user.password, password):
           session['user_id'] = user.id
           flash('Login successful!')
           return redirect(url_for('dashboard.dashboard'))
       flash('Invalid username or password.')
       return redirect(url_for('auth.login'))
   return '''
       <form method="post">
           <label for="username">Username:</label>
           <input type="text" name="username" required>
           <label for="password">Password:</label>
           <input type="password" name="password" required>
           <input type="submit" value="Log In">
       </form>
   '''
   session.pop('user_id', None)
   flash('You have been logged out.')
   return redirect(url_for('auth.login'))
