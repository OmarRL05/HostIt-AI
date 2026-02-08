<template>
  <div class="min-h-screen bg-surface-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center gap-4">
          <router-link 
            to="/orders" 
            class="text-surface-400 hover:text-brand-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </router-link>
          <div>
            <h1 class="text-2xl font-bold text-brand-900">Order Tracking</h1>
            <p class="text-sm text-surface-500 mt-1">Order #{{ orderData.orderId }}</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Tracking Summary Card -->
      <div class="card mb-6">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-lg font-semibold text-surface-800 mb-1">{{ orderData.productName }}</h2>
            <p class="text-sm text-surface-500">Sold by {{ orderData.retailer }}</p>
          </div>
          <span 
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium',
              getStatusColor(orderData.status)
            ]"
          >
            {{ orderData.status }}
          </span>
        </div>

        <!-- Delivery Estimate -->
        <div class="bg-brand-50 border border-brand-200 rounded-xl p-4 mb-6">
          <div class="flex items-start gap-3">
            <svg class="w-6 h-6 text-brand-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
            </svg>
            <div>
              <p class="font-medium text-surface-800">
                {{ orderData.status === 'Delivered' ? 'Delivered' : 'Estimated Delivery' }}
              </p>
              <p class="text-2xl font-bold text-brand-600 mt-1">{{ formatDate(orderData.estimatedDelivery) }}</p>
              <p class="text-sm text-surface-600 mt-1">{{ orderData.deliveryWindow }}</p>
            </div>
          </div>
        </div>

        <!-- Tracking Number -->
        <div class="flex items-center justify-between p-4 bg-surface-50 rounded-xl">
          <div>
            <p class="text-xs text-surface-500 uppercase mb-1">Tracking Number</p>
            <p class="font-mono text-sm font-medium text-surface-800">{{ orderData.trackingNumber }}</p>
          </div>
          <button 
            @click="copyTrackingNumber"
            class="px-3 py-1.5 text-sm text-brand-600 hover:bg-brand-50 rounded-lg transition-colors font-medium"
          >
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
        </div>
      </div>

      <!-- Tracking Timeline -->
      <div class="card">
        <h3 class="text-lg font-semibold text-brand-900 mb-6">Tracking History</h3>

        <div class="relative">
          <div class="absolute left-4 top-2 bottom-2 w-0.5 bg-surface-200"></div>

          <!-- Timeline Events -->
          <div class="space-y-6">
            <div 
              v-for="(event, index) in trackingEvents" 
              :key="index"
              class="relative flex gap-4"
            >
              <!-- Timeline Dot -->
              <div 
                :class="[
                  'relative z-10 flex items-center justify-center w-8 h-8 rounded-full border-2',
                  index === 0 
                    ? 'bg-green-500 border-green-500' 
                    : 'bg-white border-surface-300'
                ]"
              >
                <svg 
                  v-if="index === 0" 
                  class="w-5 h-5 text-white" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <div 
                  v-else 
                  :class="[
                    'w-2 h-2 rounded-full',
                    event.completed ? 'bg-gray-400' : 'bg-gray-200'
                  ]"
                ></div>
              </div>

              <!-- Event Content -->
              <div class="flex-1 pb-6">
                <div class="flex items-start justify-between">
                  <div>
                    <p 
                      :class="[
                        'font-medium',
                        index === 0 ? 'text-surface-800' : 'text-surface-700'
                      ]"
                    >
                      {{ event.status }}
                    </p>
                    <p class="text-sm text-surface-500 mt-1">{{ event.location }}</p>
                    <p class="text-xs text-surface-400 mt-1">{{ formatDateTime(event.timestamp) }}</p>
                  </div>
                  <span 
                    v-if="index === 0" 
                    class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded"
                  >
                    Latest
                  </span>
                </div>
                <p v-if="event.description" class="text-sm text-surface-600 mt-2">
                  {{ event.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Delivery Address -->
      <div class="card mt-6">
        <h3 class="text-lg font-semibold text-brand-900 mb-4">Delivery Address</h3>
        <div class="text-surface-700">
          <p class="font-medium">{{ orderData.deliveryAddress.name }}</p>
          <p class="mt-2">{{ orderData.deliveryAddress.street }}</p>
          <p>{{ orderData.deliveryAddress.city }}, {{ orderData.deliveryAddress.state }} {{ orderData.deliveryAddress.zip }}</p>
          <p class="mt-2 text-surface-500">{{ orderData.deliveryAddress.phone }}</p>
        </div>
      </div>

      <!-- Carrier Info -->
      <div class="card mt-6">
        <h3 class="text-lg font-semibold text-brand-900 mb-4">Carrier Information</h3>
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-surface-800">{{ orderData.carrier }}</p>
            <p class="text-sm text-surface-500 mt-1">Service: {{ orderData.shippingMethod }}</p>
          </div>
          <a 
            :href="orderData.carrierTrackingUrl" 
            target="_blank"
            class="inline-flex items-center gap-2 px-4 py-2 bg-brand-100 text-brand-700 rounded-xl text-sm font-medium hover:bg-brand-200 transition-colors"
          >
            Track on {{ orderData.carrier }}
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>
      </div>

      <!-- Actions -->
      <div class="mt-6 flex gap-3">
        <button 
          @click="contactSupport"
          class="btn-secondary flex-1"
        >
          Contact Support
        </button>
        <button 
          v-if="orderData.status !== 'Delivered'"
          @click="modifyDelivery"
          class="btn-secondary flex-1"
        >
          Modify Delivery
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getOrderDetail } from '@/api/orders';

const router = useRouter();
const route = useRoute();

// State
const copied = ref(false);

// Order data: from API when available, rest mock (tracking not in API yet)
const orderData = ref({
  orderId: route.params.orderId || 'ORD-2026-002',
  productName: '—',
  retailer: '—',
  status: 'In Transit',
  trackingNumber: '1Z999AA10123456784',
  carrier: 'UPS',
  shippingMethod: 'Ground',
  carrierTrackingUrl: 'https://www.ups.com/track?tracknum=1Z999AA10123456784',
  estimatedDelivery: '2026-02-09',
  deliveryWindow: 'By 8:00 PM',
  deliveryAddress: {
    name: 'John Doe',
    street: '123 Main Street, Apt 4B',
    city: 'San Francisco',
    state: 'CA',
    zip: '94102',
    phone: '+1 (555) 123-4567'
  }
});

onMounted(async () => {
  const orderId = route.params.orderId ? Number(route.params.orderId) : null;
  const itemIndex = route.params.itemId ? Number(route.params.itemId) : 0;
  if (!orderId) return;
  try {
    const { data } = await getOrderDetail(orderId);
    orderData.value.orderId = data.id;
    orderData.value.estimatedDelivery = data.delivery_date || orderData.value.estimatedDelivery;
    if (data.items && data.items.length) {
      const item = data.items[itemIndex] || data.items[0];
      orderData.value.productName = item.name;
      orderData.value.retailer = item.retailer;
      orderData.value.status = item.status || orderData.value.status;
    }
  } catch (err) {
    console.error('Error loading order for shipping:', err);
  }
});

const trackingEvents = ref([
  {
    status: 'Out for Delivery',
    location: 'San Francisco, CA',
    timestamp: '2026-02-07T08:30:00',
    description: 'Your package is out for delivery and will arrive today.',
    completed: true
  },
  {
    status: 'Arrived at Facility',
    location: 'San Francisco Distribution Center, CA',
    timestamp: '2026-02-07T05:15:00',
    completed: true
  },
  {
    status: 'In Transit',
    location: 'Oakland, CA',
    timestamp: '2026-02-06T18:45:00',
    completed: true
  },
  {
    status: 'Departed Facility',
    location: 'Seattle, WA',
    timestamp: '2026-02-06T12:00:00',
    completed: true
  },
  {
    status: 'Package Received',
    location: 'Seattle Distribution Center, WA',
    timestamp: '2026-02-05T14:30:00',
    description: 'Package received by carrier.',
    completed: true
  },
  {
    status: 'Label Created',
    location: 'Seattle, WA',
    timestamp: '2026-02-05T10:00:00',
    description: 'Shipping label has been created. Package is awaiting pickup.',
    completed: true
  }
]);

// Methods
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    weekday: 'long',
    month: 'long', 
    day: 'numeric'
  });
};

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
};

const getStatusColor = (status) => {
  const colors = {
    'In Transit': 'bg-blue-100 text-blue-800',
    'Out for Delivery': 'bg-purple-100 text-purple-800',
    'Delivered': 'bg-green-100 text-green-800',
    'Delayed': 'bg-red-100 text-red-800'
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
};

const copyTrackingNumber = () => {
  navigator.clipboard.writeText(orderData.value.trackingNumber);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};

const contactSupport = () => {
  // TODO: Implement support contact
  console.log('Contact support');
};

const modifyDelivery = () => {
  // TODO: Implement delivery modification
  console.log('Modify delivery');
};
</script>
