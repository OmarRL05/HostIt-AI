import apiClient from './client';

/**
 * Lista de órdenes del usuario.
 * @param {number} userId
 * @returns {Promise<Array<{ id: number, total: number, status: string, date: string, summary: string, items_count: number }>>}
 */
export function getUserOrders(userId) {
  return apiClient.get(`/orders/user/${userId}`);
}

/**
 * Detalle de una orden.
 * @param {number} orderId
 * @returns {Promise<{ id: number, total_cost: number, status: string, ai_summary: string, delivery_date: string, items: Array }>}
 */
export function getOrderDetail(orderId) {
  return apiClient.get(`/orders/${orderId}`);
}

/**
 * Crea una orden mock (para pruebas o checkout simulado).
 * @param {number} userId
 * @returns {Promise<{ message: string, order_id: number }>}
 */
export function createMockOrder(userId) {
  return apiClient.post('/orders/create_mock', { user_id: userId });
}
