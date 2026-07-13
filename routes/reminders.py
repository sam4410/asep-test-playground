from flask import Blueprint, request, flash, render_template, session, redirect, url_for
from your_application import db
from your_application.models import User, Invoice
from datetime import datetime, timedelta

reminder_bp = Blueprint('reminders', __name__)

@reminder_bp.route('/reminders', methods=['GET'])
def reminders():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to view reminders.')
        return redirect(url_for('auth.login'))
    
    invoices = Invoice.query.filter_by(user_id=user_id).all()
    overdue_invoices = [invoice for invoice in invoices if invoice.due_date < datetime.now() and not invoice.reminder_sent]
    
    return render_template('reminders.html', overdue_invoices=overdue_invoices)

@reminder_bp.route('/send_reminder/<int:invoice_id>', methods=['POST'])
def send_reminder(invoice_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to send reminders.')
        return redirect(url_for('auth.login'))
    
    invoice = Invoice.query.get(invoice_id)
    if invoice and invoice.user_id == user_id:
        # Logic to send email reminder (placeholder)
        # send_email(invoice.client_email, invoice)
        invoice.reminder_sent = True
        db.session.commit()
        flash('Payment reminder sent successfully!')
    else:
        flash('Invoice not found or you do not have permission to send reminders.')
    
    return redirect(url_for('reminders.reminders'))

def init_app(app):
    app.register_blueprint(reminder_bp)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    reminder_sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Invoice {self.id} for {self.client_email}>'

    def send_reminder_email(self):
        # Placeholder for actual email sending logic
        pass

    def mark_as_reminded(self):
        self.reminder_sent = True
        db.session.commit()