<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <!-- Sidebar Header -->
      <div class="p-4 border-b border-gray-200">
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-2 text-gray-600 hover:text-gray-900"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="text-sm font-medium">Cerrar sesión</span>
        </button>
      </div>

      <!-- Navigation Items -->
      <nav class="flex-1 overflow-y-auto p-4">
        <router-link 
          to="/orders" 
          class="flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-lg mb-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>My orders</span>
        </router-link>

        <button 
          @click="createNewChat"
          class="flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-lg w-full mb-4"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <span>New chat</span>
        </button>

        <!-- Chat History -->
        <div>
          <button 
            @click="toggleChatHistory"
            class="flex items-center justify-between w-full px-4 py-2 text-sm font-medium text-gray-700"
          >
            <span>Your chats</span>
            <svg 
              class="w-4 h-4 transition-transform" 
              :class="{ 'rotate-180': showChatHistory }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <div v-show="showChatHistory" class="mt-2 space-y-1">
            <div
              v-if="loadingConversations"
              class="py-2 text-center text-sm text-gray-500"
            >
              Cargando...
            </div>
            <button
              v-else
              v-for="chat in chatHistory"
              :key="chat.id"
              type="button"
              @click="selectConversation(chat.id)"
              :class="[
                'w-full text-left px-4 py-3 rounded-lg text-sm transition-colors',
                conversationId === chat.id
                  ? 'bg-blue-100 text-blue-900 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              ]"
            >
              <p class="truncate font-medium">{{ chat.title }}</p>
              <p class="text-xs text-gray-500 mt-0.5">
                {{ chat.message_count }} mensaje(s) · {{ formatChatDate(chat.created_at) }}
              </p>
            </button>
            <p v-if="!loadingConversations && chatHistory.length === 0" class="px-4 py-2 text-sm text-gray-500">
              Sin conversaciones aún
            </p>
          </div>
        </div>
      </nav>
    </aside>

    <!-- Main Chat Area -->
    <main class="flex-1 flex flex-col">
      <header class="bg-white border-b border-gray-200 px-6 py-4">
        <h1 class="text-2xl font-semibold text-gray-900">Chat</h1>
      </header>

      <!-- Messages Area -->
      <div class="flex-1 overflow-y-auto p-6">
        <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
          <div class="text-center">
            <p class="text-gray-500 text-lg mb-4">Start a conversation</p>
            <p class="text-gray-400 text-sm">Describe what you want to buy...</p>
          </div>
        </div>

        <div v-else class="max-w-4xl mx-auto space-y-6">
          <div 
            v-for="message in messages" 
            :key="message.id"
            :class="message.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
          >
            <div 
              :class="message.role === 'user' 
                ? 'bg-blue-600 text-white rounded-2xl rounded-br-sm px-4 py-3 max-w-xl' 
                : 'bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 max-w-xl shadow-sm'"
            >
              <p class="text-sm">{{ message.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="border-t border-gray-200 bg-white p-6">
        <div class="max-w-4xl mx-auto">
          <div class="relative">
            <input
              v-model="inputMessage"
              @keydown.enter="sendMessage"
              type="text"
              placeholder="Describe what you want to buy..."
              class="w-full px-6 py-4 pr-12 text-gray-700 bg-white border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button 
              @click="sendMessage"
              class="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 text-gray-400 hover:text-blue-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Products Cart Panel -->
    <aside class="w-96 bg-white border-l border-gray-200 flex flex-col">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Products</h2>
      </div>

      <!-- Cart Items -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div 
          v-for="item in cartItems" 
          :key="item.id"
          class="bg-gray-50 rounded-lg p-4 relative"
        >
          <div class="flex gap-4">
            <div class="w-16 h-16 bg-gray-200 rounded-md flex-shrink-0"></div>
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium text-gray-900 truncate">{{ item.name }}</h3>
              <p class="text-xs text-gray-500 mt-1">{{ item.retailer }}</p>
              <p class="text-sm font-semibold text-gray-900 mt-2">${{ item.price }}</p>
              <p class="text-xs text-gray-500">Delivery: {{ item.delivery }}</p>
            </div>
          </div>
          
          <div class="flex gap-2 absolute top-4 right-4">
            <button 
              @click="replaceItem(item.id)"
              class="p-1.5 text-gray-400 hover:text-blue-600 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            <button 
              @click="removeItem(item.id)"
              class="p-1.5 text-gray-400 hover:text-red-600 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Empty Cart State -->
        <div v-if="cartItems.length === 0" class="text-center py-12">
          <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <p class="text-gray-500 text-sm">Your cart is empty</p>
        </div>
      </div>

      <!-- Cart Footer -->
      <div class="border-t border-gray-200 p-6 bg-white">
        <div class="flex justify-between items-center mb-4">
          <span class="text-lg font-semibold text-gray-900">Total:</span>
          <span class="text-2xl font-bold text-gray-900">${{ cartTotal }}</span>
        </div>
        <button 
          @click="proceedToCheckout"
          :disabled="cartItems.length === 0"
          class="w-full bg-black text-white py-3 px-6 rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Checkout Now
        </button>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import {
  getOrCreateConversation,
  getConversationRecord,
  getUserConversations,
  createNewConversation,
  sendMessage as sendChatMessage
} from '@/api/chat';

const router = useRouter();
const userStore = useUserStore();

// State
const showChatHistory = ref(false);
const inputMessage = ref('');
const messages = ref([]);
const cartItems = ref([]);
const conversationId = ref(null);
const sending = ref(false);
const loadingConversations = ref(false);

const chatHistory = ref([]);

// Computed
const cartTotal = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + parseFloat(item.price), 0).toFixed(2);
});

// Methods
const loadConversationsList = async () => {
  const userId = userStore.user?.id;
  if (!userId) return;
  loadingConversations.value = true;
  try {
    const { data } = await getUserConversations(userId);
    chatHistory.value = data;
  } catch (err) {
    console.error('Error loading conversations list:', err);
    chatHistory.value = [];
  } finally {
    loadingConversations.value = false;
  }
};

const formatChatDate = (iso) => {
  if (!iso) return '';
  const d = new Date(iso);
  const now = new Date();
  const diff = now - d;
  if (diff < 86400000) return d.toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' });
  if (diff < 604800000) return d.toLocaleDateString('es', { weekday: 'short' });
  return d.toLocaleDateString('es', { day: 'numeric', month: 'short' });
};

const loadConversation = async () => {
  const userId = userStore.user?.id;
  if (!userId) return;
  try {
    const { data: conv } = await getOrCreateConversation(userId);
    conversationId.value = conv.conversation_id;
    await loadMessagesForConversation(conv.conversation_id);
    await loadConversationsList();
  } catch (err) {
    console.error('Error loading conversation:', err);
  }
};

const loadMessagesForConversation = async (convId) => {
  try {
    const { data: record } = await getConversationRecord(convId);
    messages.value = record.map((msg, i) => ({
      id: `msg-${i}-${msg.created_at}`,
      role: msg.role,
      content: msg.content
    }));
  } catch (err) {
    console.error('Error loading messages:', err);
    messages.value = [];
  }
};

const selectConversation = async (convId) => {
  conversationId.value = convId;
  await loadMessagesForConversation(convId);
};

const toggleChatHistory = () => {
  showChatHistory.value = !showChatHistory.value;
};

const createNewChat = async () => {
  const userId = userStore.user?.id;
  if (!userId) return;
  try {
    const { data } = await createNewConversation(userId);
    conversationId.value = data.conversation_id;
    messages.value = [];
    cartItems.value = [];
    await loadConversationsList();
  } catch (err) {
    console.error('Error creating new chat:', err);
  }
};

const sendMessage = async () => {
  const text = inputMessage.value.trim();
  if (!text || sending.value || !conversationId.value) return;

  const userMsg = { id: `user-${Date.now()}`, role: 'user', content: text };
  messages.value.push(userMsg);
  inputMessage.value = '';
  sending.value = true;

  try {
    const { data } = await sendChatMessage({
      conversation_id: conversationId.value,
      message: text
    });
    messages.value.push({
      id: `ai-${data.ai_message_id}`,
      role: 'assistant',
      content: data.ai_message
    });
  } catch (err) {
    console.error('Error sending message:', err);
    messages.value.push({
      id: `ai-err-${Date.now()}`,
      role: 'assistant',
      content: 'No pude enviar el mensaje. Intenta de nuevo.'
    });
  } finally {
    sending.value = false;
  }
};

const handleLogout = () => {
  userStore.logout();
  router.push('/');
};

const removeItem = (itemId) => {
  cartItems.value = cartItems.value.filter(item => item.id !== itemId);
};

const replaceItem = (itemId) => {
  console.log('Replace item:', itemId);
};

const proceedToCheckout = () => {
  router.push('/payment');
};

onMounted(() => {
  if (!userStore.user) return;
  loadConversation();
});
</script>
