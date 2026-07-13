from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from your_application import db
from your_application.models import User
import os
auth_bp = Blueprint('auth', __name__)
def init_app(app):
    app.register_blueprint(auth_bp)
    app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Use environment variable in production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    @app.before_request
    def require_login():
        if 'user_id' not in session and request.endpoint != 'auth.login' and request.endpoint != 'auth.signup':
            return redirect(url_for('auth.login'))
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')  # Placeholder for user dashboard
   
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))
    @auth_bp.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash('Username and password are required.')
                return redirect(url_for('auth.signup'))
            if User.query.filter_by(username=username).first():
                flash('Username already exists.')
                return redirect(url_for('auth.signup'))
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Sign up successful! Please log in.')
            return redirect(url_for('auth.login'))
        return render_template('signup.html')
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash('Username and password are required.')
                return redirect(url_for('auth.login'))
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.')
        return render_template('login.html')
    @auth_bp.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('You have been logged out.')
        return redirect(url_for('auth.login'))    app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Use environment variable in production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    @app.before_request
    def require_login():
        if 'user_id' not in session and request.endpoint != 'auth.login' and request.endpoint != 'auth.signup':
            return redirect(url_for('auth.login'))
    @auth_bp.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash('Username and password are required.')
                return redirect(url_for('auth.signup'))
            if User.query.filter_by(username=username).first():
                flash('Username already exists.')
                return redirect(url_for('auth.signup'))
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Sign up successful! Please log in.')
            return redirect(url_for('auth.login'))
        return render_template('signup.html')
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash('Username and password are required.')
                return redirect(url_for('auth.login'))
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.')
        return render_template('login.html')
    @auth_bp.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('You have been logged out.')
        return redirect(url_for('auth.login'))    @app.before_request
    def require_login():
        if 'user_id' not in session and request.endpoint != 'auth.login' and request.endpoint != 'auth.signup':
            return redirect(url_for('auth.login'))
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')  # Placeholder for user dashboard
   
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))        db.create_all()  # Create database tables if they don't existfrom flask import Blueprint, request, redirect, url_for, session, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from your_application import db
from your_application.models import User
import os
auth_bp = Blueprint('auth', __name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Use environment variable in production

    @app.before_request
    def require_login():
        if 'user_id' not in session and request.endpoint != 'auth.login' and request.endpoint != 'auth.signup':
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('auth.signup'))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

def init_app(app):
    app.register_blueprint(auth_bp)
    app.secret_key = 'your_secret_key'  # Use environment variable in production
    
    @app.before_request
    def require_login():
        if 'user_id' not in session and request.endpoint != 'auth.login' and request.endpoint != 'auth.signup':
            return redirect(url_for('auth.login'))

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')  # Placeholder for user dashboard

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))
    
    # Ensure to create the User model and database setup in your application
    # Example User model:
    # class User(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(80), unique=True, nullable=False)
    #     password = db.Column(db.String(128), nullable=False)