from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models.database import Order, Material, Payment

feature_bp = Blueprint('feature', __name__)

@feature_bp.route('/orders', methods=['GET', 'POST'])
def manage_orders():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        status = request.form['status']
        total = request.form['total']
        new_order = Order(customer_name=customer_name, status=status, total=total, user_id=user_id)
        db.session.add(new_order)
        db.session.commit()
        flash('Order created successfully!')
        return redirect(url_for('feature.manage_orders'))

    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('feature.html', orders=orders)

@feature_bp.route('/materials', methods=['GET', 'POST'])
def manage_materials():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        stock_level = request.form['stock_level']
        new_material = Material(name=name, stock_level=stock_level, user_id=user_id)
        db.session.add(new_material)
        db.session.commit()
        flash('Material added successfully!')
        return redirect(url_for('feature.manage_materials'))

    materials = Material.query.filter_by(user_id=user_id).all()
    return render_template('feature.html', materials=materials)

@feature_bp.route('/payments', methods=['GET'])
def view_payments():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    payments = Payment.query.filter(Payment.order.has(user_id=user_id)).all()
    return render_template('feature.html', payments=payments)