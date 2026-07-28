   user_id = session.get('user_id')
   if not user_id:
       return redirect(url_for('auth.login'))
   if request.method == 'POST':
       description = request.form['description']
       new_order = Order(description=description, user_id=user_id)
       db.session.add(new_order)
       db.session.commit()
       flash('Order created successfully!')
       return redirect(url_for('feature.manage_orders'))
   orders = Order.query.filter_by(user_id=user_id).all()
   return render_template('feature.html', orders=orders)
   order = Order.query.get_or_404(order_id)
   if order.user_id != session.get('user_id'):
       flash('You do not have permission to delete this order.')
       return redirect(url_for('feature.manage_orders'))
   db.session.delete(order)
   db.session.commit()
   flash('Order deleted successfully!')
   return redirect(url_for('feature.manage_orders'))
