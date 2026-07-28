from flask import Blueprint, render_template, session, redirect, url_for
from extensions import db
from models.database import Order, Material, Payment

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    active_orders = Order.query.filter_by(user_id=user_id).all()
    materials = Material.query.filter_by(user_id=user_id).all()
    overdue_payments = Payment.query.filter_by(status='overdue', order_id__user_id=user_id).all()

    total_active_orders = len(active_orders)
    total_materials_in_stock = sum(material.stock_level for material in materials)
    total_overdue_payments = len(overdue_payments)
    
    return render_template('dashboard.html', 
                           active_orders=active_orders, 
                           total_active_orders=total_active_orders, 
                           total_materials_in_stock=total_materials_in_stock, 
                           total_overdue_payments=total_overdue_payments)