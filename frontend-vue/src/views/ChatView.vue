<template>
  <div class="flex h-screen bg-alive gap-3 py-3 px-3">
    <!-- Sidebar -->
    <aside class="w-64 bg-white flex flex-col rounded-2xl shadow-soft overflow-hidden flex-shrink-0">
      <div class="p-5 shadow-sm">
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-2 text-[#364C40] hover:text-[#19E66E] transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="text-sm font-medium">Log Out</span>
        </button>
      </div>

      <nav class="flex-1 overflow-y-auto px-5 py-4">
        <router-link
          to="/orders"
          class="flex items-center gap-3 px-4 py-3.5 text-[#364C40] hover:bg-[#FFFEFC] hover:text-[#19E66E] rounded-xl mb-3 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>My orders</span>
        </router-link>

        <button
          @click="createNewChat"
          class="flex items-center gap-3 px-4 py-3.5 text-[#364C40] hover:bg-[#FFFEFC] hover:text-[#19E66E] rounded-xl w-full mb-5 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <span>New chat</span>
        </button>

        <div>
          <button
            @click="toggleChatHistory"
            class="flex items-center justify-between w-full px-4 py-2 text-sm font-medium text-[#364C40]"
          >
            <span>Your chats</span>
            <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': showChatHistory }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-show="showChatHistory" class="mt-2 space-y-1">
            <div v-if="loadingConversations" class="py-2 text-center text-sm text-[#364C40]/70">Cargando...</div>
            <button
              v-else
              v-for="chat in chatHistory"
              :key="chat.id"
              type="button"
              @click="selectConversation(chat.id)"
              :class="[
                'w-full text-left px-4 py-3 rounded-xl text-sm transition-colors',
                conversationId === chat.id ? 'bg-[#19E66E]/15 text-[#364C40] font-medium' : 'text-[#364C40] hover:bg-[#FFFEFC]'
              ]"
            >
              <p class="truncate font-medium">{{ chat.title }}</p>
              <p class="text-xs text-[#364C40]/70 mt-0.5">{{ chat.message_count }} mensaje(s) · {{ formatChatDate(chat.created_at) }}</p>
            </button>
            <p v-if="!loadingConversations && chatHistory.length === 0" class="px-4 py-2 text-sm text-[#364C40]/70">Sin conversaciones aún</p>
          </div>
        </div>
      </nav>
    </aside>

    <!-- Main Chat Area -->
    <main class="flex-1 flex flex-col min-w-0 backdrop-blur rounded-2xl shadow-soft overflow-hidden flex-shrink min-h-0">
      <header class="px-6 py-5 flex-shrink-0 border-[#e8e6e4]">
        <h1 class="text-2xl font-semibold text-[#364C40]">Chat</h1>
      </header>

      <!-- Connection error banner -->
      <div v-if="connectionError" class="mx-6 mt-4 mb-2 p-4 bg-red-50 border border-red-100 rounded-xl flex items-center justify-between gap-4 flex-shrink-0">
        <p class="text-sm text-red-700">{{ connectionError }}</p>
        <button @click="connectionError = ''" class="p-1.5 text-red-500 hover:bg-red-100 rounded-lg transition-colors" aria-label="Cerrar">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto px-6 py-6 min-h-0">
        <div v-if="messages.length === 0" class="flex items-center justify-center h-full min-h-[200px]">
          <div class="text-center">
            <p class="text-[#364C40] text-lg font-semibold mb-2">Start a conversation</p>
            <p class="text-[#364C40]/70 text-sm">Describe what you want to buy...</p>
          </div>
        </div>

        <div v-else class="max-w-4xl mx-auto space-y-5">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="message.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
          >
            <div
              :class="[
                'rounded-2xl px-4 py-3 max-w-xl',
                message.role === 'user'
                  ? 'bg-[#19E66E] text-white rounded-br-md'
                  : isErrorMessage(message.content)
                    ? 'bg-red-50 border border-red-100 text-red-800 rounded-bl-md'
                    : 'bg-white border border-[#e8e6e4] rounded-bl-md shadow-card'
              ]"
            >
              <p class="text-sm">{{ message.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="border-t border-[#e8e6e4] px-6 pt-5 pb-6 flex-shrink-0">
        <div class="max-w-4xl mx-auto">
          <div class="relative">
            <input
              v-model="inputMessage"
              @keydown.enter="sendMessage"
              type="text"
              placeholder="Describe what you want to buy..."
              class="input-field w-full pl-6 pr-12 py-4 rounded-full"
            />
            <button
              @click="sendMessage"
              class="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 text-[#364C40]/60 hover:text-[#19E66E] rounded-full hover:bg-[#19E66E]/10 transition-colors"
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
    <aside class="w-96 flex flex-col flex-shrink-0 rounded-2xl shadow-soft overflow-hidden bg-[#23CC8B]">
      <div class="px-6 py-5 border-b border-white/20">
        <h2 class="text-lg font-semibold text-[#FFFDF1]">Products</h2>
      </div>

      <div class="flex-1 overflow-y-auto px-6 py-6 space-y-4 min-h-0">
        <div
          v-for="item in cartItems"
          :key="item.id"
          class="bg-[#FFFEFC]/90 rounded-xl p-4 relative border border-white/30"
        >
          <div class="flex gap-4">
            <div class="w-16 h-16 bg-[#364C40]/10 rounded-lg flex-shrink-0 flex items-center justify-center">
              <svg class="w-8 h-8 text-[#364C40]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium text-[#364C40] truncate">{{ item.name }}</h3>
              <p class="text-xs text-[#364C40]/80 mt-1">{{ item.retailer }}</p>
              <p class="text-sm font-semibold text-[#364C40] mt-2">${{ item.price }}</p>
              <p class="text-xs text-[#364C40]/80">Delivery: {{ item.delivery }}</p>
            </div>
          </div>
          <div class="flex gap-2 absolute top-4 right-4">
            <button @click="replaceItem(item.id)" class="p-1.5 text-[#364C40]/70 hover:text-[#364C40] rounded-lg hover:bg-white/20 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
            </button>
            <button @click="removeItem(item.id)" class="p-1.5 text-[#364C40]/70 hover:text-red-600 rounded-lg hover:bg-white/20 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        </div>

        <div v-if="cartItems.length === 0" class="text-center py-12">
          <div class="w-16 h-16 mx-auto rounded-2xl bg-white/20 flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-[#FFFDF1]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
          </div>
          <p class="text-[#FFFDF1] text-sm font-medium">Your cart is empty</p>
        </div>
      </div>

      <!-- Cart Footer -->
      <div class="border-t border-white/20 px-6 py-6 flex-shrink-0">
        <div class="flex justify-between items-center mb-4">
          <span class="text-lg font-semibold text-[#FFFDF1]">Total:</span>
          <span class="text-2xl font-bold text-[#FFFDF1]">${{ cartTotal }}</span>
        </div>
        <button
          @click="proceedToCheckout"
          :disabled="cartItems.length === 0"
          class="w-full py-3 rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-[#FFFDF1] text-[#364C40] hover:bg-[#FFFEFC]"
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
const connectionError = ref('');

const chatHistory = ref([]);

function isErrorMessage(content) {
  if (!content || typeof content !== 'string') return false;
  const lower = content.toLowerCase();
  return lower.includes('error') || lower.includes('expecting value') || lower.includes('no pude');
}

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
  connectionError.value = '';
  try {
    const { data: conv } = await getOrCreateConversation(userId);
    conversationId.value = conv.conversation_id;
    await loadMessagesForConversation(conv.conversation_id);
    await loadConversationsList();
  } catch (err) {
    console.error('Error loading conversation:', err);
    const msg = err.response?.data?.detail || err.response?.data?.error || err.message || 'Error conectando con la IA. Revisa tu conexión.';
    connectionError.value = msg;
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
    const errMsg = err.response?.data?.detail || err.response?.data?.error || err.message || 'No pude enviar el mensaje. Intenta de nuevo.';
    connectionError.value = errMsg;
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
