# Authentication

"""
Implement a complete authentication system
"""

# Grocery Products

"""
Manage grocery products with functionality to add, update, and delete products
"""

# Email Notification System

"""
Notify users via email when the quantity of a grocery product is reduced
"""

# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/products', methods=['POST'])
def add_product():
    name = request.json.get('name')
    quantity = request.json.get('quantity')
    new_product = Product(name=name, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 201

@app.route('/reduce_quantity/<int:product_id>', methods=['PATCH'])
def reduce_quantity(product_id):
    product = Product.query.get(product_id)
    if product:
        product.quantity -= 1
        db.session.commit()
        # Send email notification
        msg = Message('Quantity Reduced', sender='your_email@gmail.com', recipients=[user.email])
        msg.body = f'The quantity of {product.name} has been reduced. New quantity: {product.quantity}'
        mail.send(msg)
        return jsonify({'message': 'Quantity reduced and notification sent'}), 200
    return jsonify({'message': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)