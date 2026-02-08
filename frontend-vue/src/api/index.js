/**
 * Capa de servicios API.
 * Todas las llamadas al backend Flask se hacen a través de estos módulos.
 */

export { default as apiClient } from './client';
export * from './auth';
export * from './users';
export * from './orders';
export { getOrCreateConversation, getConversationRecord, getUserConversations, createNewConversation, sendMessage } from './chat';
export * from './status';
