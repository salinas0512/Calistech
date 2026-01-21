<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref(null)

const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    await auth.login(email.value, password.value)
    // Redirigir según rol
    if (auth.roleId === 2) {
      router.push({ name: 'admin' })
    } else {
      router.push({ name: 'usuario' })
    }
  } catch (err) {
    error.value = 'Credenciales inválidas o error de conexión'
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <i class="fa-solid fa-arrow-left back-btn" @click="router.push('/')"></i>
      <img src="/logo500.png" alt="Logo CalisTech" class="login-logo" />
      <h1 class="login-title">Bienvenido a CalisTech</h1>
      <h2 class="login-subtitle">Inicia sesión para continuar</h2>
      <form @submit.prevent="handleLogin">
        <label>Email:</label>
        <input v-model="email" type="email" required />
        <label>Contraseña:</label>
        <input v-model="password" type="password" required />
        <button type="submit" class="login-btn">Ingresar</button>
      </form>
      <div v-if="error" class="login-error">{{ error }}</div>
      <div class="login-register">
        <span>¿No tienes cuenta?</span>
        <router-link to="/registro" class="register-link">Regístrate aquí</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6fa;
}
.login-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(67,176,42,0.10);
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.back-btn {
  position: absolute;
  top: 1.2rem;
  left: 1.2rem;
  font-size: 1.7rem;
  color: #32be16;
  cursor: pointer;
  transition: color 0.2s;
}
.back-btn:hover {
  color: #228c0f;
}
.login-logo {
  width: 140px;
  margin-bottom: 1rem;
}
.login-title {
  color: #43B02A;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.login-subtitle {
  color: #555A60;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}
form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
input {
  padding: 0.5rem;
  border: 1px solid #43B02A;
  border-radius: 6px;
  font-size: 1rem;
  background: #fff !important;
  color: #222 !important;
  box-shadow: none;
}
input::placeholder {
  color: #888 !important;
  opacity: 1;
}
input:-webkit-autofill,
input:-webkit-autofill:focus {
  -webkit-box-shadow: 0 0 0 1000px #fff inset !important;
  -webkit-text-fill-color: #222 !important;
}

@media (max-width: 600px) {
  .login-card {
    width: 97vw;
    max-width: 99vw;
    padding: 1.2rem 0.5rem 1.2rem 0.5rem;
    border-radius: 14px;
  }
  .login-title {
    font-size: 1.3rem;
  }
  .login-logo {
    width: 140px;
  }
}
.login-btn {
  background: #43B02A;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.7rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}
.login-btn:hover {
  background: #388e1c;
}
.login-register {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #555A60;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.register-link {
  color: #43B02A;
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
}
.login-error {
  color: #dc2626;
  background: #fee2e2;
  border: 1px solid #dc2626;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  margin-top: 1rem;
  font-size: 1rem;
  text-align: center;
}

/*media querys*/

@media (max-width: 600px) {
  .login-card {
    width: 85vw;
    max-width: 98vw;
    height: 75vh;
    margin: 6vw 2vw 6vw 2vw;
    padding: 1.5rem 0.7rem;
    border-radius: 14px;
  }
  .login-title {
     font-size: 2rem;
  }
}
</style>
