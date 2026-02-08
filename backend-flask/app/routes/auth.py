import email
from hmac import new
import json

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models import User

auth_bp = Blueprint('auth', __name__)

# Route to sign-up
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error':'Not enought data'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error":"email already registered"}), 400

    new_user = User(
        email=data['email'],
        full_name=data.get('full_name', 'Annonymus'),
        password_hash=generate_password_hash(data['password']), 
        shipping_address=data.get('address', ''),
        payment_method_mock=data.get('payment_info', {}) 
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message":"User Signed Up",
            "user_id":new_user.id,
            "user_email":new_user.email
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

# Route to log-in
@auth_bp.route('/api/auth/login', methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error":"Faltan Credenciales"}), 400
    
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({
            "message":"Login Complete",
            "user_id":user.id,
            "full_name":user.full_name,
            "email":user.email
        }), 200
    else:
        return jsonify({"error":"Invalid Input"}), 401