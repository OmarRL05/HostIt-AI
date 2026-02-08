import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('user', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null);

  function setUser(userData) {
    user.value = userData;
    localStorage.setItem('user', JSON.stringify(userData));
  }
  
  function logout(){
    user.value = null;
    localStorage.removeItem('user');
  }

  return { user, setUser, logout };
});