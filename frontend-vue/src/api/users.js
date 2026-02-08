import apiClient from './client';

/**
 * Obtiene el perfil del usuario.
 * @param {number} userId
 * @returns {Promise<{ id: number, email: string, full_name: string, address: string, payment_info: object }>}
 */
export function getUserProfile(userId) {
  return apiClient.get(`/users/${userId}`);
}

/**
 * Actualiza el perfil del usuario.
 * @param {number} userId
 * @param {{ full_name?: string, address?: string, payment_info?: object }} data
 * @returns {Promise<{ message: string }>}
 */
export function updateUserProfile(userId, data) {
  return apiClient.put(`/users/${userId}`, {
    full_name: data.full_name,
    address: data.address,
    payment_info: data.payment_info,
  });
}
