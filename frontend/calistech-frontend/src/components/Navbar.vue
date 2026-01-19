<template>
  <nav class="navbar">
    <div class="navbar-left">
      <img v-if="logoSrc" :src="logoSrc" alt="Logo CalisTech" class="navbar-logo" />
  
    </div>
    <div class="navbar-links">
      <router-link to="/usuario">Inicio</router-link>
      <router-link to="/perfil">Mi Perfil</router-link>
      <router-link to="/rutinas">Rutinas</router-link>
      <router-link to="/progreso">Progreso</router-link>
      <router-link to="/parques">Parques</router-link>
      <router-link v-if="isAdmin" to="/admin">Administración</router-link>
    </div>
    <button class="logout-btn" @click="logout">Cerrar sesión</button>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const auth = useAuthStore()
const router = useRouter()

const isAdmin = computed(() => auth.roleId === 2)
const logoSrc = '/logo500White.png' 

function logout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #112848f0;
  color: white;
  padding: 0.75rem 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
 
}
.navbar-left {
  display: flex;
  align-items: center;
}
.navbar-logo {
  height: 100px;
  margin-right: 1rem;
}
.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 1px;
}
.navbar-links {
  display: flex;
  gap: 1.5rem;
}
.navbar-links a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.navbar-links a.router-link-exact-active,
.navbar-links a:hover {
  color: #3bcd1e;
  border-bottom: none;
}
.logout-btn {
  background: #32be16;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 1.5rem;
  transition: background 0.2s;
}
.logout-btn:hover {
  background: #228c0f;
}
</style>
