from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('materials', lazy=True))

def create_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def create_order(name, status, user_id):
    new_order = Order(name=name, status=status, user_id=user_id)
    db.session.add(new_order)
    db.session.commit()
    return new_order

def create_material(name, quantity, user_id):
    new_material = Material(name=name, quantity=quantity, user_id=user_id)
    db.session.add(new_material)
    db.session.commit()
    return new_material