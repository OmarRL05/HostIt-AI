from email import message
from re import M
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import ChatMessage, User, Conversation
import requests
import os

chat_bp = Blueprint('chat', __name__)
N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')

# List all conversations for a user
@chat_bp.route('/api/chat/user/<int:user_id>', methods=['GET'])
def list_conversations(user_id):
    convos = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.created_at.desc()).all()
    return jsonify([{
        "id": c.id,
        "title": c.title or "New Chat",
        "status": c.status,
        "created_at": c.created_at.isoformat(),
        "message_count": len(c.messages)
    } for c in convos]), 200

# Start a new conversation (close current open, create new)
@chat_bp.route('/api/chat/new', methods=['POST'])
def new_conversation():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    active = Conversation.query.filter_by(user_id=user_id, status='open').first()
    if active:
        active.status = 'closed'
        db.session.commit()
    new_conv = Conversation(user_id=user_id)
    db.session.add(new_conv)
    db.session.commit()
    return jsonify({
        "conversation_id": new_conv.id,
        "status": new_conv.status
    }), 201

# Get or create the current open conversation
@chat_bp.route('/api/chat/conversation', methods=['POST'])
def get_or_create():
    data = request.get_json()
    user_id = data.get('user_id') # User ID

    active_chat = Conversation.query.filter_by(user_id=user_id, status='open').first()

    if not active_chat:
        active_chat = Conversation(user_id=user_id)
        db.session.add(active_chat)
        db.session.commit()
        is_new = True
    else:
        is_new = False
    
    return jsonify({
        "conversation_id": active_chat.id,
        "is_new": is_new,
        "status": active_chat.status
    }), 200

# Send a message
@chat_bp.route('/api/chat/message', methods=["POST"])
def send_message():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    user_content = data.get('message')
    
    # 1. Guardar mensaje del Usuario (Rápido, para que quede en historial)
    user_msg = ChatMessage(conversation_id=conversation_id, role='user', content=user_content)
    db.session.add(user_msg)
    db.session.commit()
    
    # 2. Enviar a n8n para procesamiento INTELIGENTE
    ai_response_text = "Lo siento, mi cerebro está desconectado."
    
    try:
        # Enviamos contexto: ID de conversación y el mensaje
        payload = {
            "sessionId":conversation_id,
            "userId": user_msg.id,
            "chatInput": user_content
        }
        
        # Llamada a n8n
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            n8n_data = response.json()
            # n8n debe devolver un JSON: { "text": "Hola..." }
            ai_response_text = n8n_data.get('text', 'Sin respuesta de IA')
        else:
            ai_response_text = f"Error en n8n: {response.status_code}"

    except Exception as e:
        ai_response_text = f"Error conectando con la IA: {str(e)}"

    # 3. Guardar respuesta del Asistente
    ai_msg = ChatMessage(conversation_id=conversation_id, role='assistant', content=ai_response_text)
    db.session.add(ai_msg)
    db.session.commit()
    
    return jsonify({
        "user_message_id": user_msg.id,
        "ai_message": ai_response_text,
        "ai_message_id": ai_msg.id
    })

# Look for the record of the chat
@chat_bp.route('/api/chat/<int:conversation_id>', methods=["GET"])
def get_record(conversation_id):
    messages =  ChatMessage.query.filter_by(conversation_id=conversation_id).order_by(ChatMessage.created_at).all()

    return jsonify([{
        "role": msg.role,
        "content": msg.content,
        "created_at": msg.created_at.isoformat()
    } for msg in messages]), 200
