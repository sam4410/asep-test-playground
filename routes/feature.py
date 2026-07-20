from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from extensions import db
from models.database import Order

feature_bp = Blueprint('feature', __name__)

@feature_bp.route('/feature/create', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    user_id = session['user_id']
    name = request.form['name']
    status = request.form['status']

    new_order = Order(name=name, status=status, user_id=user_id)
    db.session.add(new_order)
    db.session.commit()

    flash('Order created successfully')
    return redirect(url_for('dashboard.dashboard'))

@feature_bp.route('/feature/orders')
def list_orders():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('feature.html', orders=orders)

@feature_bp.route('/feature/update/<int:order_id>', methods=['POST'])
def update_order(order_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    order = Order.query.get(order_id)
    if not order:
        flash('Order not found.')
        return redirect(url_for('dashboard.dashboard'))

    order.status = request.form['status']
    db.session.commit()

    flash('Order updated successfully')
    return redirect(url_for('dashboard.dashboard'))

@feature_bp.route('/feature/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    order = Order.query.get(order_id)
    if not order:
        flash('Order not found.')
        return redirect(url_for('dashboard.dashboard'))

    db.session.delete(order)
    db.session.commit()

    flash('Order deleted successfully')
    return redirect(url_for('dashboard.dashboard'))