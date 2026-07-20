from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models.database import Order, Material, OrderMaterial

feature_bp = Blueprint('feature', __name__)

@feature_bp.route('/feature', methods=['GET', 'POST'])
def feature():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        description = request.form['description']
        materials = request.form.getlist('materials')
        quantities = request.form.getlist('quantities')

        new_order = Order(description=description, user_id=session['user_id'])
        db.session.add(new_order)
        db.session.commit()

        for material_id, quantity in zip(materials, quantities):
            order_material = OrderMaterial(order_id=new_order.id, material_id=material_id, quantity=quantity)
            db.session.add(order_material)

        db.session.commit()
        flash('Order created successfully!')
        return redirect(url_for('feature.feature'))

    materials = Material.query.all()
    return render_template('feature.html', materials=materials)