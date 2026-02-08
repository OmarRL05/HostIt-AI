import apiClient from './client';

/**
 * Obtiene o crea la conversación activa del usuario.
 * @param {number} userId
 * @returns {Promise<{ conversation_id: number, is_new: boolean, status: string }>}
 */
export function getOrCreateConversation(userId) {
  return apiClient.post('/chat/conversation', { user_id: userId });
}

/**
 * Envía un mensaje en la conversación.
 * @param {{ conversation_id: number, message: string }} data
 * @returns {Promise<{ user_message_id: number, ai_message: string, ai_message_id: number }>}
 */
export function sendMessage(data) {
  return apiClient.post('/chat/message', {
    conversation_id: data.conversation_id,
    message: data.message,
  });
}

/**
 * Obtiene el historial de mensajes de una conversación.
 * @param {number} conversationId
 * @returns {Promise<Array<{ role: string, content: string, created_at: string }>>}
 */
export function getConversationRecord(conversationId) {
  return apiClient.get(`/chat/${conversationId}`);
}
