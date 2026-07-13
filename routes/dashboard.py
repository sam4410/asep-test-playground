from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from your_application import db
from your_application.models import Invoice
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to view the dashboard.')
        return redirect(url_for('auth.login'))
    
    invoices = Invoice.query.filter_by(user_id=user_id).all()
    overdue_invoices = [invoice for invoice in invoices if invoice.due_date < datetime.now() and not invoice.reminder_sent]
    
    return render_template('dashboard.html', invoices=invoices, overdue_invoices=overdue_invoices)

def init_app(app):
    app.register_blueprint(dashboard_bp)
    
    @app.before_request
    def require_login():
        if 'user_id' not in session and request.endpoint != 'auth.login' and request.endpoint != 'auth.signup':
            return redirect(url_for('auth.login'))
    
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))