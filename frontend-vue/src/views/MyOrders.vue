<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <router-link 
              to="/chat" 
              class="text-gray-400 hover:text-gray-600"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </router-link>
            <h1 class="text-2xl font-bold text-gray-900">My Orders</h1>
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
                  ? 'bg-black text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
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
      <!-- Empty State -->
      <div v-if="filteredOrders.length === 0" class="text-center py-16">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gray-100 rounded-full mb-6">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">No orders found</h3>
        <p class="text-gray-500 mb-6">Start shopping to see your orders here</p>
        <router-link 
          to="/chat" 
          class="inline-flex items-center gap-2 bg-black text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          Start Shopping
        </router-link>
      </div>

      <!-- Orders List -->
      <div v-else class="space-y-6">
        <div 
          v-for="order in filteredOrders" 
          :key="order.id"
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
        >
          <!-- Order Header -->
          <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-6">
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Order ID</p>
                  <p class="font-mono text-sm font-medium text-gray-900">{{ order.id }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Date</p>
                  <p class="text-sm font-medium text-gray-900">{{ formatDate(order.date) }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Total</p>
                  <p class="text-sm font-bold text-gray-900">${{ order.total.toFixed(2) }}</p>
                </div>
              </div>

              <!-- Status Badge -->
              <span 
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium',
                  getStatusColor(order.status)
                ]"
              >
                {{ order.status }}
              </span>
            </div>
          </div>

          <!-- Order Items -->
          <div class="p-6">
            <div class="space-y-4">
              <div 
                v-for="item in order.items" 
                :key="item.id"
                class="flex gap-4"
              >
                <div class="w-20 h-20 bg-gray-100 rounded-lg flex-shrink-0 overflow-hidden">
                  <img 
                    v-if="item.image" 
                    :src="item.image" 
                    :alt="item.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                
                <div class="flex-1 min-w-0">
                  <h4 class="font-medium text-gray-900 mb-1">{{ item.name }}</h4>
                  <p class="text-sm text-gray-500 mb-2">{{ item.retailer }}</p>
                  <div class="flex items-center gap-4 text-sm">
                    <span class="text-gray-600">Qty: {{ item.quantity }}</span>
                    <span class="text-gray-900 font-medium">${{ item.price.toFixed(2) }}</span>
                  </div>
                </div>

                <!-- Tracking Button -->
                <div v-if="order.status === 'Shipped'" class="flex items-center">
                  <button 
                    @click="trackOrder(order.id, item.id)"
                    class="text-blue-600 hover:text-blue-700 text-sm font-medium"
                  >
                    Track Package
                  </button>
                </div>
              </div>
            </div>

            <!-- Delivery Info -->
            <div v-if="order.deliveryDate" class="mt-6 pt-6 border-t border-gray-200">
              <div class="flex items-center gap-2 text-sm">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                </svg>
                <span class="text-gray-700">
                  <span class="font-medium">
                    {{ order.status === 'Delivered' ? 'Delivered on' : 'Estimated delivery' }}:
                  </span>
                  {{ formatDate(order.deliveryDate) }}
                </span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 flex gap-3">
              <button 
                @click="viewOrderDetails(order.id)"
                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                View Details
              </button>
              <button 
                v-if="order.status === 'Delivered'"
                @click="reorder(order.id)"
                class="flex-1 px-4 py-2 bg-black text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
              >
                Buy Again
              </button>
              <button 
                v-if="['Processing', 'Shipped'].includes(order.status)"
                @click="cancelOrder(order.id)"
                class="px-4 py-2 border border-red-300 text-red-600 rounded-lg text-sm font-medium hover:bg-red-50 transition-colors"
              >
                Cancel Order
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// State
const activeFilter = ref('all');

const orderStatuses = [
  { label: 'All', value: 'all' },
  { label: 'Processing', value: 'Processing' },
  { label: 'Shipped', value: 'Shipped' },
  { label: 'Delivered', value: 'Delivered' }
];

// Mock orders data
const orders = ref([
  {
    id: 'ORD-2026-001',
    date: '2026-02-05',
    status: 'Delivered',
    total: 345.99,
    deliveryDate: '2026-02-06',
    items: [
      {
        id: 'item-1',
        name: 'Columbia Powder Keg II Jacket',
        retailer: 'Amazon',
        quantity: 1,
        price: 189.99,
        image: null
      },
      {
        id: 'item-2',
        name: 'The North Face Ski Pants',
        retailer: 'REI',
        quantity: 1,
        price: 156.00,
        image: null
      }
    ]
  },
  {
    id: 'ORD-2026-002',
    date: '2026-02-06',
    status: 'Shipped',
    total: 89.99,
    deliveryDate: '2026-02-09',
    items: [
      {
        id: 'item-3',
        name: 'Smartwool Merino Wool Socks',
        retailer: 'Backcountry',
        quantity: 2,
        price: 44.99,
        image: null
      },
      {
        id: 'item-4',
        name: 'Outdoor Research Gloves',
        retailer: 'Moosejaw',
        quantity: 1,
        price: 45.00,
        image: null
      }
    ]
  },
  {
    id: 'ORD-2026-003',
    date: '2026-02-07',
    status: 'Processing',
    total: 129.99,
    deliveryDate: '2026-02-10',
    items: [
      {
        id: 'item-5',
        name: 'Smith Optics Snow Goggles',
        retailer: 'Evo',
        quantity: 1,
        price: 129.99,
        image: null
      }
    ]
  }
]);

// Computed
const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') {
    return orders.value;
  }
  return orders.value.filter(order => order.status === activeFilter.value);
});

// Methods
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
};

const getStatusColor = (status) => {
  const colors = {
    'Processing': 'bg-yellow-100 text-yellow-800',
    'Shipped': 'bg-blue-100 text-blue-800',
    'Delivered': 'bg-green-100 text-green-800',
    'Cancelled': 'bg-red-100 text-red-800'
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
};

const viewOrderDetails = (orderId) => {
  router.push(`/orders/${orderId}`);
};

const trackOrder = (orderId, itemId) => {
  router.push(`/shipping/${orderId}/${itemId}`);
};

const reorder = (orderId) => {
  // TODO: Implement reorder logic
  console.log('Reorder:', orderId);
};

const cancelOrder = (orderId) => {
  // TODO: Implement cancel order logic
  if (confirm('Are you sure you want to cancel this order?')) {
    console.log('Cancel order:', orderId);
  }
};
</script>
