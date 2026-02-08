import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/user'

// View imports
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

router.beforeEach((to, from) => {
  const userStore = useUserStore()
  const publicPages = ['login', 'register']
  const authRequired = !publicPages.includes(to.name)

  // Redirect to login if trying to access protected page without auth
  if (authRequired && !userStore.user) {
    return { name: 'login' }
  }

  // Redirect to chat if logged in user tries to access login/register
  if (publicPages.includes(to.name) && userStore.user) {
    return { name: 'chat' }
  }
})

export default router
