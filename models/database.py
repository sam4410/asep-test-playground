from your_application import db
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    reminder_sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Invoice {self.id} for {self.client_email}>'

def create_user(username, password):
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def create_invoice(user_id, client_email, due_date):
    new_invoice = Invoice(user_id=user_id, client_email=client_email, due_date=due_date)
    db.session.add(new_invoice)
    db.session.commit()
    return new_invoice

def get_invoices_by_user(user_id):
    return Invoice.query.filter_by(user_id=user_id).all()
    def __repr__(self):
        return f'<User {self.username}>'

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    reminder_sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Invoice {self.id} for {self.client_email}>'

def create_user(username, password):
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def create_invoice(user_id, client_email, due_date):
    new_invoice = Invoice(user_id=user_id, client_email=client_email, due_date=due_date)
    db.session.add(new_invoice)
    db.session.commit()
    return new_invoice

def get_invoices_by_user(user_id):
    return Invoice.query.filter_by(user_id=user_id).all()