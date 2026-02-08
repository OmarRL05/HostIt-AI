<template>
<div class="min-h-screen bg-surface-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <router-link 
              to="/chat" 
              class="text-surface-400 hover:text-brand-600 transition-colors"
            >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </router-link>
            <h1 class="text-2xl font-bold text-brand-900">My Orders</h1>
          </div>
          
          <!-- Filter Tabs -->
          <div class="flex gap-2">
            <button
              v-for="status in orderStatuses"
              :key="status.value"
              @click="activeFilter = status.value"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                activeFilter === status.value
                  ? 'bg-brand-600 text-white'
                  : 'bg-surface-100 text-surface-700 hover:bg-surface-200'
              ]"
            >
              {{ status.label }}
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Detail View (single order) -->
      <template v-if="orderIdParam">
        <div v-if="loadingDetail" class="text-center py-12">Cargando...</div>
        <div v-else-if="orderDetail" class="space-y-6">
          <button
            @click="router.push('/orders')"
            class="flex items-center gap-2 text-surface-600 hover:text-brand-600 mb-4 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Volver a mis órdenes
          </button>
          <div class="card overflow-hidden">
            <div class="bg-surface-50 px-6 py-4 border-b border-surface-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-6">
                  <div>
                    <p class="text-xs text-surface-500 uppercase mb-1">Order ID</p>
                    <p class="font-mono text-sm font-medium text-surface-800">{{ orderDetail.id }}</p>
                  </div>
                <div v-if="orderDetail.delivery_date">
                  <p class="text-xs text-surface-500 uppercase mb-1">Entrega estimada</p>
                  <p class="text-sm font-medium text-surface-800">{{ formatDate(orderDetail.delivery_date) }}</p>
                </div>
                  <div>
                    <p class="text-xs text-surface-500 uppercase mb-1">Total</p>
                    <p class="text-sm font-bold text-surface-800">${{ Number(order.total).toFixed(2) }}</p>
                  </div>
                </div>
                <span :class="['px-4 py-2 rounded-full text-sm font-medium', getStatusColor(orderDetail.status)]">
                  {{ formatStatus(orderDetail.status) }}
                </span>
              </div>
            </div>
            <div class="p-6">
              <p v-if="orderDetail.ai_summary" class="text-sm text-surface-600 mb-4">{{ orderDetail.ai_summary }}</p>
              <p v-if="orderDetail.delivery_date" class="text-sm text-surface-700 mb-4">
                Entrega estimada: {{ formatDate(orderDetail.delivery_date) }}
              </p>
              <h3 class="text-sm font-semibold text-brand-900 mb-3">Productos</h3>
              <div class="space-y-4">
                <div
                  v-for="(item, idx) in detailItems"
                  :key="idx"
                  class="flex gap-4 items-center p-3 bg-surface-50 rounded-xl"
                >
                  <div class="w-20 h-20 bg-brand-100 rounded-lg flex-shrink-0 flex items-center justify-center">
                    <svg class="w-8 h-8 text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <h4 class="font-medium text-surface-800">{{ item.name }}</h4>
                    <p class="text-sm text-surface-500">{{ item.retailer }}</p>
                    <p class="text-sm font-medium text-brand-700">${{ Number(item.price).toFixed(2) }}</p>
                  </div>
                  <span :class="['px-2 py-1 rounded-lg text-xs font-medium', getStatusColor(item.status) || 'bg-surface-100 text-surface-700']">
                    {{ item.status }}
                  </span>
                  <button
                    v-if="formatStatus(orderDetail.status) === 'Shipped'"
                    @click="trackOrder(orderDetail.id, idx)"
                    class="text-brand-600 hover:text-brand-700 text-sm font-medium"
                  >
                    Track
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- List View -->
      <template v-else>
        <div v-if="loading" class="text-center py-12">Cargando órdenes...</div>
        <div v-else-if="filteredOrders.length === 0" class="text-center py-16">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-brand-100 rounded-full mb-6">
            <svg class="w-10 h-10 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-brand-900 mb-2">No orders found</h3>
          <p class="text-surface-500 mb-6">Start shopping to see your orders here</p>
          <router-link
            to="/chat"
            class="btn-primary inline-flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            Start Shopping
          </router-link>
        </div>

        <div v-else class="space-y-6">
          <div
            v-for="order in filteredOrders"
            :key="order.id"
            class="card overflow-hidden hover:shadow-soft transition-shadow"
          >
            <div class="bg-surface-50 px-6 py-4 border-b border-surface-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-6">
                  <div>
                    <p class="text-xs text-surface-500 uppercase mb-1">Order ID</p>
                    <p class="font-mono text-sm font-medium text-surface-800">{{ order.id }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-surface-500 uppercase mb-1">Date</p>
                    <p class="text-sm font-medium text-surface-800">{{ formatDate(order.date) }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-surface-500 uppercase mb-1">Total</p>
                    <p class="text-sm font-bold text-surface-800">${{ Number(order.total).toFixed(2) }}</p>
                  </div>
                </div>
                <span :class="['px-4 py-2 rounded-full text-sm font-medium', getStatusColor(order.status)]">
                  {{ formatStatus(order.status) }}
                </span>
              </div>
            </div>
            <div class="p-6">
              <p v-if="order.summary" class="text-sm text-surface-600 mb-2">{{ order.summary }}</p>
              <p class="text-sm text-surface-500 mb-4">{{ order.items_count }} item(s)</p>
              <div class="flex gap-3">
                <button
                  @click="viewOrderDetails(order.id)"
                  class="btn-secondary flex-1 py-2"
                >
                  View Details
                </button>
                <button
                  v-if="formatStatus(order.status) === 'Delivered'"
                  @click="reorder(order.id)"
                  class="btn-primary flex-1 py-2"
                >
                  Buy Again
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { getUserOrders, getOrderDetail } from '@/api/orders';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// State
const activeFilter = ref('all');
const orders = ref([]);
const orderDetail = ref(null);
const loading = ref(false);
const loadingDetail = ref(false);

const orderStatuses = [
  { label: 'All', value: 'all' },
  { label: 'Processing', value: 'Processing' },
  { label: 'Shipped', value: 'Shipped' },
  { label: 'Delivered', value: 'Delivered' }
];

const orderIdParam = computed(() => route.params.orderId ? Number(route.params.orderId) : null);

// Computed
const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') return orders.value;
  return orders.value.filter(order => formatStatus(order.status) === activeFilter.value);
});

const detailItems = computed(() => {
  const order = orderDetail.value;
  if (!order || !Array.isArray(order.items)) return [];
  return order.items;
});

// Methods
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

const formatStatus = (status) => {
  const map = { completed: 'Delivered', simulated_pending: 'Processing' };
  return map[status] || status || 'Processing';
};

const getStatusColor = (status) => {
  const display = formatStatus(status);
  const colors = {
    'Processing': 'bg-yellow-100 text-yellow-800',
    'Shipped': 'bg-blue-100 text-blue-800',
    'Delivered': 'bg-green-100 text-green-800',
    'Cancelled': 'bg-red-100 text-red-800'
  };
  return colors[display] || 'bg-gray-100 text-gray-800';
};

const loadOrders = async () => {
  const userId = userStore.user?.id;
  if (!userId) return;
  loading.value = true;
  try {
    const { data } = await getUserOrders(userId);
    orders.value = data;
  } catch (err) {
    console.error('Error loading orders:', err);
    orders.value = [];
  } finally {
    loading.value = false;
  }
};

const loadOrderDetail = async (id) => {
  loadingDetail.value = true;
  orderDetail.value = null;
  try {
    const { data } = await getOrderDetail(id);
    orderDetail.value = data;
  } catch (err) {
    console.error('Error loading order detail:', err);
  } finally {
    loadingDetail.value = false;
  }
};

const viewOrderDetails = (orderId) => {
  router.push(`/orders/${orderId}`);
};

const trackOrder = (orderId, itemId) => {
  router.push(`/shipping/${orderId}/${itemId}`);
};

const reorder = (orderId) => {
  console.log('Reorder:', orderId);
};

onMounted(() => {
  if (orderIdParam.value) {
    loadOrderDetail(orderIdParam.value);
  } else {
    loadOrders();
  }
});

watch(orderIdParam, (id) => {
  if (id) loadOrderDetail(id);
  else {
    orderDetail.value = null;
    loadOrders();
  }
});
</script>
