import apiClient from './client';

/**
 * Registro de usuario.
 * @param {{ email: string, password: string, full_name?: string, address?: string, payment_info?: object }} data
 * @returns {Promise<{ user_id: number, user_email: string }>}
 */
export function register(data) {
  return apiClient.post('/auth/register', {
    email: data.email,
    password: data.password,
    full_name: data.full_name ?? data.name,
    address: data.address,
    payment_info: data.payment_info,
  });
}

/**
 * Inicio de sesión.
 * @param {{ email: string, password: string }} data
 * @returns {Promise<{ user_id: number, full_name: string, email: string }>}
 */
export function login(data) {
  return apiClient.post('/auth/login', {
    email: data.email,
    password: data.password,
  });
}
