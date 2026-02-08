from .extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    shipping_address = db.Column(db.Text, nullable=True) 
    payment_method_mock = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    conversations = db.relationship('Conversation', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True)
    specs = db.relationship('ShoppingSpecs', backref='conversation', uselist=False, lazy=True)

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShoppingSpecs(db.Model):
    __tablename__ = 'shopping_specs'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)

    budget = db.Column(db.Float, nullable=True) 
    deadline = db.Column(db.String(100), nullable=True) 
    
    preferences = db.Column(JSON, nullable=True)
    
    must_haves = db.Column(JSON, nullable=True)

    candidates = db.relationship('ProductCandidate', backref='specs', lazy=True)

class ProductCandidate(db.Model):
    __tablename__ = 'product_candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.Integer, db.ForeignKey('shopping_specs.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    retailer_name = db.Column(db.String(50), nullable=False) 
    product_url = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    
    delivery_estimate = db.Column(db.String(100), nullable=True)
    
    rank_score = db.Column(db.Integer, default=0) 
    rank_explanation = db.Column(db.Text, nullable=True) 
    
    is_selected = db.Column(db.Boolean, default=False)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    spec_id = db.Column(db.Integer, db.ForeignKey('shopping_specs.id'), nullable=True)
    
    total_cost = db.Column(db.Float, nullable=False)
    
    checkout_status = db.Column(db.String(50), default='simulated_pending')
    
    pdf_receipt_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    retailer = db.Column(db.String(50), nullable=False)
    
    retailer_status = db.Column(db.String(50), default='pending')