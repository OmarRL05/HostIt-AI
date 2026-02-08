import json
from re import I
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Order, OrderItem, User

orders_bp = Blueprint('order', __name__)

# list of users order
@orders_bp.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_user_order(user_id):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    results = []
    for order in orders:
        results.append({
            "id": order.id,
            "total": order.total_cost,
            "status": order.checkout_status,
            "date": order.created_at.isoformat(),
            "summary": order.ai_summary,
            "items_count": len(order.items)
        })
    return jsonify(results), 200

# Order Details
@orders_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    items_data = [{
        "name": i.product_name,
        "price": i.price,
        "retailer": i.retailer,
        "status": i.retailer_status
    }for i in order.items]

    return jsonify({
        "id": order.id,
        "total": order.total_cost,
        "status": order.checkout_status,
        "ai_summary": order.ai_summary,
        "delivery_date": order.estimated_delivery_global,
        "items": items_data
    }), 200



# function to fill fields at the database
@orders_bp.route('/api/orders/create_mock', methods=['POST'])
def create_mock_order():
    data = request.get_json()
    user_id = data.get('user_id')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # 1. Crear Orden Dummy
    new_order = Order(
        user_id=user.id,
        total_cost=1850.50,
        checkout_status='completed',
        ai_summary="Outfit casual para fiesta de SuperBowl. Incluye Jersey y accesorios.",
        estimated_delivery_global="2026-02-14"
    )
    db.session.add(new_order)
    db.session.commit()
    
    # 2. Agregar Items Dummy
    items = [
        OrderItem(order_id=new_order.id, product_name="Jersey Chiefs Rojo Talla M", price=1200.00, retailer="Nike Store", retailer_status="confirmed"),
        OrderItem(order_id=new_order.id, product_name="Gorra New Era Negra", price=650.50, retailer="Amazon", retailer_status="shipping")
    ]
    db.session.add_all(items)
    db.session.commit()
    
    return jsonify({
        "message": "Orden Mock creada exitosamente",
        "order_id": new_order.id
    }), 201