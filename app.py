from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    quantity = db.Column(db.Integer)

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Other proposal fields

# Initialize DB
db.create_all()

# Email Notification Function
def send_email(subject, body, receivers):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

# User Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Logged in"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

# Product Routes
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added"}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    if product:
        product.name = data['name']
        product.quantity = data['quantity']
        db.session.commit()
        return jsonify({"message": "Product updated"}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/products/<int:id>/reduce_quantity', methods=['POST'])
def reduce_quantity(id):
    data = request.json
    product = Product.query.get(id)
    if product and product.quantity >= data['quantity']:
        product.quantity -= data['quantity']
        db.session.commit()
        
        # Send email notification
        send_email("Product Quantity Reduced", 
                   f"Reduced quantity of {product.name} by {data['quantity']}. New quantity: {product.quantity}",
                   ["Jeevaperumal1128@gmail.com", data['buyer_email']])
        
        return jsonify({"message": "Quantity reduced"}), 200
    return jsonify({"message": "Product not found or insufficient quantity"}), 404

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "quantity": p.quantity} for p in products]), 200

# Existing Proposal Routes
# (Add your existing routes here)

if __name__ == '__main__':
    app.run(debug=True)
