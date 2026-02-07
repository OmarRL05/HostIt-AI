from flask import Blueprint, jsonify

base_bp = Blueprint('base', __name__)

@base_bp.route('/api/status', methods=['GET'])
def server_status():
    return jsonify({
        'status': 'online',
        'message': 'Server is running',
        'service': 'AI Agent Commerce API'
    })