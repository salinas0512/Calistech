<template>
  <div class="registro-container">
    <div class="registro-card">
      <i class="fa-solid fa-arrow-left back-btn" @click="router.push('/')"></i>
      <img src="/logo500.png" alt="Logo CalisTech" class="registro-logo" />
      <h1 class="registro-title">Registro en CalisTech</h1>
      <form @submit.prevent="handleRegister">
        <label>Nombre de usuario:</label>
        <input v-model="nombre" type="text" required :class="{ invalid: !isNombreValid && nombre }" />
        <div v-if="nombre && !isNombreValid" class="field-error">El nombre no puede estar vacío.</div>
        <label>Email:</label>
        <input v-model="email" type="email" required :class="{ invalid: !isEmailValid && email }" />
        <div v-if="email && !isEmailValid" class="field-error">Ingresa un email válido.</div>
        <label>Contraseña:</label>
        <input v-model="password" type="password" required :class="{ invalid: !isPasswordValid && password }" />
        <div v-if="password && !isPasswordValid" class="field-error">La contraseña debe tener entre 5 y 72 caracteres.</div>
        <button type="submit" class="registro-btn" :disabled="!isFormValid">Registrarse</button>
      </form>
      <div v-if="error" class="registro-error">{{ error }}</div>
      <div v-if="success" class="registro-success">
        ¡Registro exitoso! Redirigiendo al login...
        <span class="spinner"></span>
      </div>
      <div class="registro-login">
        <span>¿Ya tienes cuenta?</span>
        <router-link to="/login" class="login-link">Inicia sesión aquí</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const email = ref('')
const password = ref('')
const nombre = ref('')
const error = ref(null)
const success = ref(false)
const router = useRouter()

const isEmailValid = computed(() => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value))
const isPasswordValid = computed(() => password.value.length >= 5 && password.value.length <= 72)
const isNombreValid = computed(() => nombre.value.trim().length > 0)
const isFormValid = computed(() => isEmailValid.value && isPasswordValid.value && isNombreValid.value)

async function handleRegister() {
  error.value = null
  success.value = false
  if (!isFormValid.value) {
    error.value = 'Completa todos los campos correctamente.'
    return
  }
  try {
    await axios.post('https://calistech.onrender.com/usuarios/registro', {
      nombre: nombre.value,
      email: email.value,
      contrasena: password.value,
      rol_id: 1
    })
    success.value = true
    setTimeout(() => router.push('/login'), 2500)
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Error al registrar. Intenta nuevamente.'
    }
  }
}
</script>

<style scoped>
.registro-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6fa;
}
.registro-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(67,176,42,0.10);
  padding: 2.5rem 2rem;
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.registro-logo {
  width: 80px;
  margin-bottom: 1rem;
}
.registro-title {
  color: #43B02A;
  font-size: 2rem;
  font-weight: bold;
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
}
input.invalid {
  border: 1.5px solid #dc2626;
  background: #fee2e2;
}
.registro-btn {
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
.registro-btn:hover {
  background: #388e1c;
}
button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.registro-login {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #555A60;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.login-link {
  color: #0072BC;
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
}
.registro-error {
  color: #dc2626;
  background: #fee2e2;
  border: 1px solid #dc2626;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  margin-top: 1rem;
  font-size: 1rem;
  text-align: center;
}
.registro-success {
  color: #43B02A;
  background: #e6fbe6;
  border: 1px solid #43B02A;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  margin-top: 1rem;
  font-size: 1rem;
  text-align: center;
}
.field-error {
  color: #dc2626;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  margin-top: -0.5rem;
  text-align: left;
  width: 100%;
}
.spinner {
  display: inline-block;
  width: 22px;
  height: 22px;
  border: 3px solid #43B02A;
  border-top: 3px solid #e6fbe6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-left: 10px;
  vertical-align: middle;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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
</style>
