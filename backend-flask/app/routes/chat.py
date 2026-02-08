from email import message
from re import M
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import ChatMessage, User, Conversation
import requests
import os

chat_bp = Blueprint('chat', __name__)

# Get conversation
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
    user_content = data.get('message') #json from front has to have "message" as the key of the message

    if not conversation_id or not user_content:
        return jsonify({"error":"Missing Data"}), 400
    
    user_msg = ChatMessage(
        conversation_id=conversation_id,
        role='user',
        content=user_content
    )

    db.session.add(user_msg)
    db.session.commit()

    # n8n is being introduced here later
    ai_response_text = f'Message catched: {user_content}...'
    # ....

    ai_msg = ChatMessage(
        conversation_id=conversation_id,
        role='assistant',
        content=ai_response_text
    )
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify({
        "user_message_id":user_msg.id,
        "ai_message":ai_response_text,
        "ai_message_id":ai_msg.id
    }), 201

# Look for the record of the chat
@chat_bp.route('/api/chat/<int:conversation_id>', methods=["GET"])
def get_record(conversation_id):
    messages =  ChatMessage.query.filter_by(conversation_id=conversation_id).order_by(ChatMessage.created_at).all()

    return jsonify([{
        "role": msg.role,
        "content": msg.content,
        "created_at": msg.created_at.isoformat()
    } for msg in messages]), 200
