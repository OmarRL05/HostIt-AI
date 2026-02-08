<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center gap-4">
          <router-link 
            to="/chat" 
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </router-link>
          <h1 class="text-2xl font-bold text-gray-900">Checkout</h1>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column - Forms -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Contact Information -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">Contact Information</h2>
              <span class="text-sm text-gray-500">Step 1 of 3</span>
            </div>
            
            <div class="space-y-4">
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                  Email address
                </label>
                <input
                  id="email"
                  v-model="contactInfo.email"
                  type="email"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="you@example.com"
                />
              </div>
              
              <div>
                <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                  Phone number
                </label>
                <input
                  id="phone"
                  v-model="contactInfo.phone"
                  type="tel"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="+1 (555) 000-0000"
                />
              </div>
            </div>
          </div>

          <!-- Shipping Address -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">Shipping Address</h2>
              <span class="text-sm text-gray-500">Step 2 of 3</span>
            </div>
            
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
                    First name
                  </label>
                  <input
                    id="firstName"
                    v-model="shippingAddress.firstName"
                    type="text"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
                
                <div>
                  <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
                    Last name
                  </label>
                  <input
                    id="lastName"
                    v-model="shippingAddress.lastName"
                    type="text"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
              </div>

              <div>
                <label for="address" class="block text-sm font-medium text-gray-700 mb-2">
                  Address
                </label>
                <input
                  id="address"
                  v-model="shippingAddress.address"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="123 Main Street"
                />
              </div>

              <div>
                <label for="apartment" class="block text-sm font-medium text-gray-700 mb-2">
                  Apartment, suite, etc. (optional)
                </label>
                <input
                  id="apartment"
                  v-model="shippingAddress.apartment"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="Apt 4B"
                />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label for="city" class="block text-sm font-medium text-gray-700 mb-2">
                    City
                  </label>
                  <input
                    id="city"
                    v-model="shippingAddress.city"
                    type="text"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
                
                <div>
                  <label for="state" class="block text-sm font-medium text-gray-700 mb-2">
                    State
                  </label>
                  <select
                    id="state"
                    v-model="shippingAddress.state"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  >
                    <option value="">Select state</option>
                    <option value="CA">California</option>
                    <option value="NY">New York</option>
                    <option value="TX">Texas</option>
                    <!-- Add more states -->
                  </select>
                </div>
              </div>

              <div>
                <label for="zipCode" class="block text-sm font-medium text-gray-700 mb-2">
                  ZIP code
                </label>
                <input
                  id="zipCode"
                  v-model="shippingAddress.zipCode"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="94102"
                />
              </div>

              <label class="flex items-center gap-2">
                <input
                  v-model="saveAddress"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span class="text-sm text-gray-700">Save this address for future orders</span>
              </label>
            </div>
          </div>

          <!-- Payment Method -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">Payment Method</h2>
              <span class="text-sm text-gray-500">Step 3 of 3</span>
            </div>

            <!-- Payment Method Tabs -->
            <div class="flex gap-2 mb-6">
              <button
                v-for="method in paymentMethods"
                :key="method.id"
                @click="selectedPaymentMethod = method.id"
                :class="[
                  'flex-1 px-4 py-3 rounded-lg border-2 transition-all',
                  selectedPaymentMethod === method.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <div class="flex items-center justify-center gap-2">
                  <component :is="method.icon" class="w-5 h-5" />
                  <span class="font-medium text-sm">{{ method.name }}</span>
                </div>
              </button>
            </div>

            <!-- Credit Card Form -->
            <div v-if="selectedPaymentMethod === 'card'" class="space-y-4">
              <div>
                <label for="cardNumber" class="block text-sm font-medium text-gray-700 mb-2">
                  Card number
                </label>
                <div class="relative">
                  <input
                    id="cardNumber"
                    v-model="paymentInfo.cardNumber"
                    type="text"
                    required
                    maxlength="19"
                    @input="formatCardNumber"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    placeholder="1234 5678 9012 3456"
                  />
                  <div class="absolute right-3 top-1/2 -translate-y-1/2 flex gap-1">
                    <img src="https://js.stripe.com/v3/fingerprinted/img/visa-729c05c240c4bdb47b03ac81d9945bfe.svg" alt="Visa" class="h-6" />
                    <img src="https://js.stripe.com/v3/fingerprinted/img/mastercard-4d8844094130711885b5e41b28c9848f.svg" alt="Mastercard" class="h-6" />
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label for="expiry" class="block text-sm font-medium text-gray-700 mb-2">
                    Expiry date
                  </label>
                  <input
                    id="expiry"
                    v-model="paymentInfo.expiry"
                    type="text"
                    required
                    maxlength="5"
                    @input="formatExpiry"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    placeholder="MM/YY"
                  />
                </div>
                
                <div>
                  <label for="cvv" class="block text-sm font-medium text-gray-700 mb-2">
                    CVV
                  </label>
                  <input
                    id="cvv"
                    v-model="paymentInfo.cvv"
                    type="text"
                    required
                    maxlength="4"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    placeholder="123"
                  />
                </div>
              </div>

              <div>
                <label for="cardName" class="block text-sm font-medium text-gray-700 mb-2">
                  Cardholder name
                </label>
                <input
                  id="cardName"
                  v-model="paymentInfo.cardName"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="John Doe"
                />
              </div>

              <label class="flex items-center gap-2">
                <input
                  v-model="savePaymentMethod"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span class="text-sm text-gray-700">Save payment method for future purchases</span>
              </label>
            </div>

            <!-- PayPal -->
            <div v-else-if="selectedPaymentMethod === 'paypal'" class="text-center py-8">
              <svg class="w-16 h-16 mx-auto text-blue-600 mb-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M7.076 21.337H2.47a.641.641 0 0 1-.633-.74L4.944.901C5.026.382 5.474 0 5.998 0h7.46c2.57 0 4.578.543 5.69 1.81 1.01 1.15 1.304 2.42 1.012 4.287-.023.143-.047.288-.077.437-.983 5.05-4.349 6.797-8.647 6.797h-2.19c-.524 0-.968.382-1.05.9l-1.12 7.106zm14.146-14.42a3.35 3.35 0 0 0-.607-.541c-.013.076-.026.175-.041.254-.93 4.778-4.005 7.201-9.138 7.201h-2.19a.563.563 0 0 0-.556.479l-1.187 7.527h-.506l-.24 1.516a.56.56 0 0 0 .554.647h3.882c.46 0 .85-.334.922-.788.06-.26.76-4.852.816-5.09a.932.932 0 0 1 .923-.788h.58c3.76 0 6.705-1.528 7.565-5.946.36-1.847.174-3.388-.777-4.471z"/>
              </svg>
              <p class="text-gray-600 mb-4">You will be redirected to PayPal to complete your purchase</p>
              <button class="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
                Continue with PayPal
              </button>
            </div>
          </div>
        </div>

        <!-- Right Column - Order Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-8">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Order Summary</h2>

            <!-- Order Items -->
            <div class="space-y-4 mb-6">
              <div 
                v-for="item in orderItems" 
                :key="item.id"
                class="flex gap-3"
              >
                <div class="w-16 h-16 bg-gray-100 rounded-lg flex-shrink-0"></div>
                <div class="flex-1 min-w-0">
                  <h4 class="text-sm font-medium text-gray-900 truncate">{{ item.name }}</h4>
                  <p class="text-xs text-gray-500 mt-1">{{ item.retailer }}</p>
                  <div class="flex items-center justify-between mt-2">
                    <span class="text-xs text-gray-600">Qty: {{ item.quantity }}</span>
                    <span class="text-sm font-medium text-gray-900">${{ item.price.toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Price Breakdown -->
            <div class="border-t border-gray-200 pt-4 space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Subtotal</span>
                <span class="text-gray-900 font-medium">${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Shipping</span>
                <span class="text-gray-900 font-medium">
                  {{ shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}` }}
                </span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Tax</span>
                <span class="text-gray-900 font-medium">${{ tax.toFixed(2) }}</span>
              </div>
              
              <!-- Discount -->
              <div v-if="discount > 0" class="flex justify-between text-sm text-green-600">
                <span>Discount</span>
                <span>-${{ discount.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Total -->
            <div class="border-t border-gray-200 pt-4 mt-4">
              <div class="flex justify-between items-center">
                <span class="text-lg font-semibold text-gray-900">Total</span>
                <span class="text-2xl font-bold text-gray-900">${{ total.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Promo Code -->
            <div class="mt-6">
              <button 
                @click="showPromoCode = !showPromoCode"
                class="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                {{ showPromoCode ? 'Hide' : 'Have a promo code?' }}
              </button>
              
              <div v-if="showPromoCode" class="mt-3 flex gap-2">
                <input
                  v-model="promoCode"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="Enter code"
                />
                <button 
                  @click="applyPromoCode"
                  class="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
                >
                  Apply
                </button>
              </div>
            </div>

            <!-- Place Order Button -->
            <button 
              @click="placeOrder"
              :disabled="processing"
              class="w-full mt-6 bg-black text-white py-4 px-6 rounded-lg font-semibold hover:bg-gray-800 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              <span v-if="!processing">Place Order</span>
              <span v-else class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            </button>

            <!-- Security Badge -->
            <div class="mt-4 flex items-center justify-center gap-2 text-xs text-gray-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>Secure checkout powered by Stripe</span>
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
const processing = ref(false);
const saveAddress = ref(false);
const savePaymentMethod = ref(false);
const showPromoCode = ref(false);
const promoCode = ref('');
const discount = ref(0);

const selectedPaymentMethod = ref('card');
const paymentMethods = [
  { id: 'card', name: 'Card', icon: 'CreditCardIcon' },
  { id: 'paypal', name: 'PayPal', icon: 'PayPalIcon' }
];

const contactInfo = ref({
  email: '',
  phone: ''
});

const shippingAddress = ref({
  firstName: '',
  lastName: '',
  address: '',
  apartment: '',
  city: '',
  state: '',
  zipCode: ''
});

const paymentInfo = ref({
  cardNumber: '',
  expiry: '',
  cvv: '',
  cardName: ''
});

const orderItems = ref([
  {
    id: 1,
    name: 'Columbia Powder Keg II Jacket',
    retailer: 'Amazon',
    quantity: 1,
    price: 189.99
  },
  {
    id: 2,
    name: 'The North Face Ski Pants',
    retailer: 'REI',
    quantity: 1,
    price: 156.00
  },
  {
    id: 3,
    name: 'Smartwool Merino Wool Socks',
    retailer: 'Backcountry',
    quantity: 2,
    price: 44.99
  }
]);

// Computed
const subtotal = computed(() => {
  return orderItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

const shipping = computed(() => {
  return subtotal.value > 100 ? 0 : 9.99;
});

const tax = computed(() => {
  return subtotal.value * 0.0875; // 8.75% tax rate
});

const total = computed(() => {
  return subtotal.value + shipping.value + tax.value - discount.value;
});

// Methods
const formatCardNumber = (e) => {
  let value = e.target.value.replace(/\s/g, '');
  let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
  paymentInfo.value.cardNumber = formattedValue;
};

const formatExpiry = (e) => {
  let value = e.target.value.replace(/\//g, '');
  if (value.length >= 2) {
    paymentInfo.value.expiry = value.slice(0, 2) + '/' + value.slice(2, 4);
  } else {
    paymentInfo.value.expiry = value;
  }
};

const applyPromoCode = () => {
  // TODO: Validate promo code with backend
  if (promoCode.value.toUpperCase() === 'SAVE10') {
    discount.value = subtotal.value * 0.1;
  }
};

const placeOrder = async () => {
  processing.value = true;

  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Simulate successful order
    const orderId = 'ORD-' + Date.now();
    
    // Redirect to success page
    router.push(`/orders/${orderId}?success=true`);
  } catch (error) {
    console.error('Order failed:', error);
    alert('Payment failed. Please try again.');
  } finally {
    processing.value = false;
  }
};
</script>
