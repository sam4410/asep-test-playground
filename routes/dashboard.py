from flask import Blueprint, render_template, session, redirect, url_for
from extensions import db
from models.database import Order, Material

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    user_orders = Order.query.filter_by(user_id=session['user_id']).all()
    total_orders = len(user_orders)
    pending_payments = sum(1 for order in user_orders if order.payment_status == 'Pending')
    materials_in_stock = Material.query.all()
    total_materials = sum(material.quantity for material in materials_in_stock)

    return render_template('dashboard.html', 
                           total_orders=total_orders, 
                           pending_payments=pending_payments, 
                           total_materials=total_materials, 
                           user_orders=user_orders)