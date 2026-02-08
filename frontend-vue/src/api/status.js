import apiClient from './client';

/**
 * Comprueba que el backend esté en línea.
 * @returns {Promise<{ status: string, message: string, service: string }>}
 */
export function getStatus() {
  return apiClient.get('/status');
}
