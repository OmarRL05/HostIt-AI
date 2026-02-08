<template>
  <div class="min-h-screen bg-gradient-to-br from-brand-50 via-white to-accent-50 flex items-center justify-center py-10 px-6">
    <div class="w-full max-w-md">
      <!-- Logo/Brand -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center w-18 h-18 bg-gradient-to-br from-brand-500 to-brand-700 rounded-2xl p-4 mb-6 shadow-soft">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-brand-900">Agentic Commerce</h1>
        <p class="text-brand-600/80 mt-2 text-sm">AI-powered shopping assistant</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white/90 backdrop-blur rounded-2xl shadow-soft border border-surface-100 py-10 px-8 sm:px-10">
        <h2 class="text-2xl font-bold text-surface-800 mb-8">Sign In</h2>

        <!-- Error Message -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-100 rounded-xl">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-surface-700 mb-3">Email address</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="input-field"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-surface-700 mb-3">Password</label>
            <div class="relative">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-field pr-12"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-surface-400 hover:text-brand-600 transition-colors"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center cursor-pointer">
              <input
                v-model="formData.rememberMe"
                type="checkbox"
                class="w-4 h-4 text-brand-600 border-surface-300 rounded focus:ring-brand-500"
              />
              <span class="ml-2 text-sm text-surface-600">Remember me</span>
            </label>
            <a href="#" class="text-sm text-brand-600 hover:text-brand-700 font-medium">Forgot password?</a>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn-primary w-full py-3.5"
          >
            <span v-if="!loading">Sign In</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
          </button>
        </form>

        <p class="mt-8 text-center text-sm text-surface-600">
          Don't have an account?
          <router-link to="/register" class="text-brand-600 hover:text-brand-700 font-semibold ml-1">Sign up</router-link>
        </p>
      </div>

      <p class="text-center text-sm text-surface-400 mt-10">© 2026 Agentic Commerce</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '@/api/auth';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const userStore = useUserStore();

const loading = ref(false);
const error = ref('');
const showPassword = ref(false);

const formData = ref({
  email: '',
  password: '',
  rememberMe: false
});

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    const { data } = await login({
      email: formData.value.email,
      password: formData.value.password
    });
    userStore.setUser({
      id: data.user_id,
      email: data.email,
      full_name: data.full_name
    });
    router.push('/chat');
  } catch (err) {
    error.value = err.response?.data?.error || err.message || 'Error al iniciar sesión';
  } finally {
    loading.value = false;
  }
};
</script>
