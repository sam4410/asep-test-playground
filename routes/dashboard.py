   user_id = session.get('user_id')
   if not user_id:
       return redirect(url_for('auth.login'))
   active_orders = Order.query.filter_by(user_id=user_id).all()
   materials = Material.query.all()
   return render_template('dashboard.html', orders=active_orders, materials=materials)
