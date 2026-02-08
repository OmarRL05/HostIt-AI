import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue'
import ChatView from '@/views/ChatView.vue'
import RegisterView from '@/views/RegisterView.vue'
import MyOrders from '@/views/MyOrders.vue'
import Shipping from '@/views/Shipping.vue'
import Payment from '@/views/Payment.vue' 


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
    path: '/orders',
    name: 'MyOrders',
    component: MyOrders,
    },
    {
      path: '/orders/:orderId',
      name: 'OrderDetails',
      component: MyOrders,
    },
    {
      path: '/shipping/:orderId/:itemId?',
      name: 'Shipping',
      component: Shipping,
      
    },
    {
      path: '/payment',
      name: 'Payment',
      component: Payment,
      
    }
  ],
})

export default router
