from collections import UserDict
from turtle import st
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User

user_bp = Blueprint('user', __name__)

# to get profile details
@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.shipping_address,
        "payment_info": user.payment_method_mock or {}
    }), 200

# to update profile details
@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'address' in data:
        user.shipping_address = data['address']
    if 'payment_info' in data:
        user.payment_method_mock = data['payment_info']
    
    try:
        db.session.commit()
        return jsonify({"message":"Proflie updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500