from flask import Blueprint, request, session, redirect, url_for, flash
from extensions import db
from models.database import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        flash('Username already exists.')
        return redirect(url_for('auth.signup_page'))
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash('Successfully signed up')
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['user_id'] = user.id
        flash('Logged in successfully')
        return redirect(url_for('dashboard.dashboard'))
    flash('Invalid username or password')
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully')
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/login')
def login_page():
    return '<form method="POST" action="/login">...</form>'  # Replace with actual login form HTML

@auth_bp.route('/signup')
def signup_page():
    return '<form method="POST" action="/signup">...</form>'  # Replace with actual signup form HTML