<script setup>
import { useAuthStore } from './store/auth'
import { useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>



<template>
  <div id="app">
    <Navbar v-if="auth.isAuthenticated" />
    <div class="centered-container">
      <router-view />
    </div>
  </div>
</template>

<script setup>

</script>

<style>

html, body, #app {
  font-family: system-ui, Arial, sans-serif;
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  background: #f4f6fa;
  box-sizing: border-box;
}

.centered-container {
  width: 100vw;
  flex-direction: column;
  align-items: center;

  box-sizing: border-box;
}

.app-header {
  background: #1f2937;
  color: white;
  padding: 1rem;
  text-align: center;
  width: 100%;
  border-radius: 8px 8px 0 0;
  margin-bottom: 1rem;
}

.logout-btn {
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 2rem;
  transition: background 0.2s;
}
.logout-btn:hover {
  background: #b91c1c;
}
</style>
