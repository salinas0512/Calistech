<script setup>
import { useAuthStore } from './store/auth'
import { useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { ref, onMounted, onUnmounted } from 'vue'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/')
}

const showScrollTop = ref(false)
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
function handleScroll() {
  showScrollTop.value = window.scrollY > 200
}
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>



<template>
  <div id="app">
    <Navbar v-if="auth.isAuthenticated" />
    <div class="centered-container">
      <router-view />
    </div>
    <button v-show="showScrollTop" class="scroll-top-btn" @click="scrollToTop" title="Ir arriba">
      <i class="fa-solid fa-circle-chevron-up" style="color: #32be16; font-size: 2.1rem;"></i>
    </button>
  </div>

</template>

<style>
.scroll-top-btn {
  position: fixed;
  right: 2.2rem;
  bottom: 2.2rem;
  z-index: 1000;
  background: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 2px 12px rgba(67,176,42,0.13);
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.18s, box-shadow 0.18s;
  opacity: 0.93;
}
.scroll-top-btn:hover {
  background: #e6fbe6;
  box-shadow: 0 4px 18px rgba(67,176,42,0.18);
  opacity: 1;
}

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
  width: 100%;
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
