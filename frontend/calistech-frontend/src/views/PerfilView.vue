<template>
  <div class="perfil-container">
    <div class="perfil-card">
      <div class="perfil-avatar-section">
        <div class="perfil-avatar-wrapper">
          <img class="perfil-avatar" :src="user.fotoPerfil || defaultAvatar" alt="Foto de perfil" />
        </div>
        <button class="perfil-btn perfil-btn-foto" @click="cambiarFoto">Cambiar foto</button>
      </div>
      <div class="perfil-info">
        <h2 class="perfil-nombre">{{ user.nombre }}</h2>
        <p class="perfil-email"><i class="fa-solid fa-envelope"></i> {{ user.email }}</p>
        <p class="perfil-rol"><i class="fa-solid fa-user"></i> Rol: {{ user.rol }}</p>
        <p class="perfil-fecha"><i class="fa-solid fa-calendar"></i> Registrado: {{ user.fechaRegistro }}</p>
      </div>
      <div class="perfil-extra">
        <div class="perfil-objetivo">
          <label>Objetivo personal:</label>
          <span v-if="!editandoObjetivo">{{ user.objetivo || 'No definido' }}</span>
          <select v-else v-model="nuevoObjetivo">
            <option v-for="op in objetivos" :key="op" :value="op">{{ op }}</option>
          </select>
          <button class="perfil-btn perfil-btn-mini" v-if="!editandoObjetivo" @click="editarObjetivo">Seleccionar</button>
          <button class="perfil-btn perfil-btn-mini" v-else @click="guardarObjetivo">Guardar</button>
        </div>
        <div class="perfil-nivel">
          <label>Nivel actual:</label>
          <span v-if="!editandoNivel">{{ user.nivel || 'No definido' }}</span>
          <select v-else v-model="nuevoNivel">
            <option v-for="nivel in niveles" :key="nivel" :value="nivel">{{ nivel }}</option>
          </select>
          <button class="perfil-btn perfil-btn-mini" v-if="!editandoNivel" @click="editarNivel">Seleccionar</button>
          <button class="perfil-btn perfil-btn-mini" v-else @click="guardarNivel">Guardar</button>
        </div>
      </div>
      <div class="perfil-acciones">
        <button class="perfil-btn perfil-btn-secundario" @click="cambiarContrasena">Cambiar contraseña</button>
        <button class="perfil-btn perfil-btn-peligro" @click="mostrarModalEliminar = true">Eliminar cuenta</button>
        <!-- Modal de confirmación para eliminar cuenta -->
        <div v-if="mostrarModalEliminar" class="modal-eliminar-overlay">
          <div class="modal-eliminar">
            <h3 v-if="!eliminandoCuenta">¿Eliminar cuenta?</h3>
            <p v-if="!eliminandoCuenta">Esta acción no se puede deshacer. ¿Seguro que quieres eliminar tu cuenta?</p>
            <div v-if="!eliminandoCuenta" class="modal-eliminar-btns">
              <button class="perfil-btn perfil-btn-peligro" @click="confirmarEliminarCuenta">Eliminar</button>
              <button class="perfil-btn perfil-btn-secundario" @click="mostrarModalEliminar = false">Cancelar</button>
            </div>
            <!-- Estado de eliminación -->
            <div v-if="eliminandoCuenta" class="modal-eliminar-estado">
              <div class="spinner"></div>
              <p class="modal-eliminar-mensaje">
                <span v-if="!mensajeExito">Eliminando cuenta...</span>
                <span v-else style="color:#e74c3c;font-weight:600;">{{ mensajeExito }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="perfil-progreso">
        <h3>Resumen de progreso</h3>
        <p>Has completado {{ user.rutinasMes || 0 }} rutinas este mes.</p>
        <div class="perfil-insignias">
          <span class="insignia">🏅 Constante</span>
          <span class="insignia">🔥 7 días seguidos</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Modal de confirmación para eliminar cuenta
const mostrarModalEliminar = ref(false)
const eliminandoCuenta = ref(false)
const mensajeExito = ref('')

async function confirmarEliminarCuenta() {
  eliminandoCuenta.value = true
  try {
    await api.delete('/usuarios/eliminar-cuenta')
    mensajeExito.value = 'Cuenta eliminada correctamente. Redirigiendo...'
    setTimeout(() => {
      auth.logout()
      router.push('/')
    }, 2500) // delay igual al registro exitoso
  } catch (e) {
    mensajeError.value = 'Error al eliminar la cuenta. Intenta nuevamente.'
    setTimeout(() => { mensajeError.value = '' }, 2000)
  } finally {
    setTimeout(() => {
      mostrarModalEliminar.value = false
      eliminandoCuenta.value = false
      mensajeExito.value = ''
    }, 2500)
  }
}
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import api from '../services/api'
import { useRouter } from 'vue-router'
const defaultAvatar = '/perfil.png'
const user = ref({})
const auth = useAuthStore()

// Opciones fijas para nivel y objetivo
const niveles = ['Principiante', 'Intermedio', 'Avanzado']
const objetivos = ['Bajar de peso', 'Ganar músculo', 'Mantenimiento', 'Mejorar fuerza']

const editandoNivel = ref(false)
const editandoObjetivo = ref(false)
const nuevoNivel = ref('')
const nuevoObjetivo = ref('')

async function fetchUserProfile() {
  try {
    if (auth.user && auth.user.id) {
      const { data } = await api.get(`/usuarios/${auth.user.id}`)
      const rolFromApi = (typeof data.rol === 'string' && data.rol) || (data.rol && data.rol.nombre) || data.role || (data.role && data.role.name) || data.rol_nombre || data.rolName
      user.value = {
        fotoPerfil: data.fotoPerfil || '',
        nombre: data.nombre,
        email: data.email,
        rol: rolFromApi || auth.user?.rol || '',
        fechaRegistro: data.created_at ? data.created_at.split('T')[0] : '',
        objetivo: data.objetivo || '',
        nivel: data.nivel || '',
        preferencias: data.preferencias || '',
        rutinasMes: data.rutinasMes || 0
      }
      nuevoNivel.value = user.value.nivel
      nuevoObjetivo.value = user.value.objetivo
    }
  } catch (e) {
    user.value = { nombre: 'Error al cargar', email: '', rol: '', fechaRegistro: '', objetivo: '', nivel: '', preferencias: '', rutinasMes: 0 }
  }
}

onMounted(fetchUserProfile)

function cambiarFoto() { /* lógica para subir foto */ }
function cambiarContrasena() { /* lógica para cambiar contraseña */ }

/* Eliminar cuenta */
const router = useRouter()
async function eliminarCuenta() {
  const seguro = confirm('¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer.');
  if (!seguro) return;
  try {
    await api.delete('/usuarios/eliminar-cuenta')
    alert('Cuenta eliminada correctamente. ¡Hasta pronto!')
    auth.logout()
    router.push('/')
  } catch (e) {
    alert('Error al eliminar la cuenta. Intenta nuevamente.')
  }
}
function editarObjetivo() { editandoObjetivo.value = true }
function guardarObjetivo() {
  user.value.objetivo = nuevoObjetivo.value
  editandoObjetivo.value = false
  // Aquí luego se hará el POST/PUT al backend
}
function editarNivel() { editandoNivel.value = true }
function guardarNivel() {
  user.value.nivel = nuevoNivel.value
  editandoNivel.value = false
  // Aquí luego se hará el POST/PUT al backend
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
/* Modal de eliminación */
.modal-eliminar-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-eliminar {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 4px 24px rgba(67,176,42,0.13);
  padding: 2rem 2.2rem 1.5rem 2.2rem;
  text-align: center;
  max-width: 340px;
}
.modal-eliminar h3 {
  color: #e74c3c;
  font-size: 1.25rem;
  margin-bottom: 0.7rem;
}
.modal-eliminar-btns {
  display: flex;
  justify-content: center;
  gap: 1.2rem;
  margin-top: 1.2rem;
}

.perfil-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6fa;
}
.perfil-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(67,176,42,0.10);
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 420px;
  width: 100%;
}
.perfil-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.2rem;
}
.perfil-avatar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
}
.perfil-avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  border: none;
  background: #f4f6fa;
  box-shadow: 0 2px 8px rgba(67,176,42,0.08);
}
.perfil-btn {
  background: #32be16;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  margin: 0.2rem 0.3rem;
  cursor: pointer;
  transition: background 0.2s;
}
.perfil-btn:hover {
  background: #228c0f;
}
.perfil-btn-foto {
  font-size: 0.95rem;
  padding: 0.4rem 1rem;
}
.perfil-btn-mini {
  font-size: 0.92rem;
  padding: 0.3rem 0.7rem;
  margin-left: 0.5rem;
}
.perfil-btn-secundario {
  background: #112848;
}
.perfil-btn-secundario:hover {
  background: #0a1830;
}
.perfil-btn-peligro {
  background: #e74c3c;
}
.perfil-btn-peligro:hover {
  background: #c0392b;
}
.perfil-info {
  text-align: center;
  margin-bottom: 1.2rem;
}
.perfil-nombre {
  font-size: 1.5rem;
  font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
  font-weight: bold;
  color: #32be16;
  margin-bottom: 0.2rem;
}
.perfil-email, .perfil-rol, .perfil-fecha {
  color: #555A60;
  font-size: 1.05rem;
  margin-bottom: 0.2rem;
}
.perfil-extra {
  width: 100%;
  margin-bottom: 1.2rem;
}
.perfil-extra label {
  font-weight: 600;
  color: #32be16;
  margin-right: 0.3rem;
}
.perfil-objetivo, .perfil-nivel, .perfil-preferencias {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.perfil-acciones {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.7rem;
  margin-bottom: 1.2rem;
}
.perfil-progreso {
  width: 100%;
  background: #f4f6fa;
  border-radius: 10px;
  padding: 1rem 1.5rem;
  text-align: center;
  color: #112848;
  font-size: 1.05rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
}
.perfil-progreso h3 {
  color: #32be16;
  font-size: 1.1rem;
  margin-bottom: 0.3rem;
}
.perfil-insignias {
  margin-top: 0.5rem;
}
.insignia {
  display: inline-block;
  background: #32be16;
  color: #fff;
  border-radius: 12px;
  padding: 0.2rem 0.8rem;
  font-size: 0.98rem;
  margin: 0 0.2rem;
  font-weight: 600;
}
.spinner {
  margin: 0 auto 1rem auto;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #e74c3c;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  animation: spin 0.9s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.modal-eliminar-estado {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 1.2rem;
}
.modal-eliminar-mensaje {
  color: #e74c3c;
  font-weight: 600;
  font-size: 1.08rem;
  margin-top: 0.5rem;
  text-align: center;
}
</style>
