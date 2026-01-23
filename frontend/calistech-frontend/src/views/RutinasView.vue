<template>
  <div class="rutinas-dashboard-hero">
    <div class="rutinas-hero-overlay">
      <div class="rutinas-hero-content">
        <h1 class="rutinas-hero-title">Mis Rutinas</h1>
        <p class="rutinas-hero-subtitle">Organiza y crear tus nuevas rutinas calisténicas</p>
        <button class="rutinas-btn" @click="mostrarFormulario = true">+ Nueva rutina</button>
      </div>
    </div>
  </div>
  <div class="rutinas-container">
    <div class="rutinas-wrapper">
      <div v-if="cargando">Cargando rutinas...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else-if="rutinas.length === 0" class="sin-rutinas-msg">
        Aún no tienes rutinas creadas. ¡Haz clic en "Nueva rutina" para comenzar!
      </div>
      <template v-else>
        <div class="tarjeta" v-for="rutina in rutinas" :key="rutina.id">
          <div class="rutina-card-header">
            <h3>{{ rutina.nombre }}</h3>
            <div class="rutina-actions">
              <button class="icon-btn" @click="abrirEditarRutina(rutina)" title="Editar">
                <i class="fa-solid fa-pen-to-square"></i>
              </button>
              <button class="icon-btn" @click="eliminarRutina(rutina.id)" title="Eliminar">
                <i class="fa-solid fa-trash-can"></i>
              </button>
            </div>
          </div>
          <div class="rutina-timer-row">
            <span class="rutina-timer-label">Duración: {{ rutina.duracion }} min</span>
            <button class="timer-play-btn" @click="iniciarTemporizador(rutina)">
              <i class="fa-solid fa-play"></i>
            </button>
          </div>
          <div v-if="temporizadorActivo && rutinaTemporizadorId === rutina.id" class="timer-box">
            <span class="timer-tiempo">{{ formatoTiempo(temporizadorRestante) }}</span>
            <button class="timer-control-btn" @click="pausarTemporizador" v-if="!temporizadorPausado">
              <i class="fa-solid fa-pause"></i>
            </button>
            <button class="timer-control-btn" @click="reanudarTemporizador" v-if="temporizadorPausado">
              <i class="fa-solid fa-play"></i>
            </button>
            <button class="timer-control-btn" @click="reiniciarTemporizador">
              <i class="fa-solid fa-rotate-left"></i>
            </button>
            <button class="timer-control-btn" @click="finalizarTemporizador">
              <i class="fa-solid fa-stop"></i>
            </button>
          </div>
          <p>Nivel: {{ rutina.nivel }}</p>
          <p v-if="rutina.ejercicios">Ejercicios: {{ rutina.ejercicios.length }}</p>
          <button class="rutinas-btn-secundario" @click="verDetalleRutina(rutina)">Ver detalles</button>
        </div>
      </template>
    </div>
  </div>

    <!-- Modal/Formulario para crear rutina -->
    <div v-if="mostrarFormulario" class="modal-bg">
      <div class="modal-form responsive-modal">
        <h3>{{ editandoRutina ? 'Editar rutina' : 'Crear nueva rutina' }}</h3>
        <form class="modal-form-content" @submit.prevent="editandoRutina ? guardarEdicionRutina() : crearRutina()">
          <label>Nombre:</label>
          <input v-model="nuevaRutina.nombre" type="text" required />
          <label>Nivel:</label>
          <select v-model="nuevaRutina.nivel">
            <option value="Principiante">Principiante</option>
            <option value="Intermedio">Intermedio</option>
            <option value="Avanzado">Avanzado</option>
          </select>
          <label>Duración (minutos):</label>
          <input v-model.number="nuevaRutina.duracion" type="number" min="1" required />
          <br/>
          <label style="font-weight: bold; font-size: 20px;">Ejercicios</label>
          <div class="ejercicios-list">
            <div v-for="ej in ejerciciosApi" :key="ej.id" class="ejercicio-checkbox">
              <input type="checkbox" :id="'ej-'+ej.id" :value="ej.nombre" :checked="!!ejerciciosSeleccionados.find(e => e.nombre === ej.nombre)" @change="toggleEjercicio(ej.nombre)" />
              <label :for="'ej-'+ej.id">{{ ej.nombre }}</label>
            </div>
          </div>
          <div v-if="ejerciciosSeleccionados.length" class="tabla-ejercicios">
            <table>
              <thead>
                <tr>
                  <th>Ejercicio</th>
                  <th>Reps</th>
                  <th>Series</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ej in ejerciciosSeleccionados" :key="ej.nombre">
                  <td>{{ ej.nombre }}</td>
                  <td>
                    <div class="control-flex">
                      <button type="button" @click="cambiarReps(ej.nombre, -1)">-</button>
                      <span class="contador">{{ ej.reps }}</span>
                      <button type="button" @click="cambiarReps(ej.nombre, 1)">+</button>
                    </div>
                  </td>
                  <td>
                    <div class="control-flex">
                      <button type="button" @click="cambiarSeries(ej.nombre, -1)">-</button>
                      <span class="contador">{{ ej.series }}</span>
                      <button type="button" @click="cambiarSeries(ej.nombre, 1)">+</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="formError" class="form-error">{{ formError }}</div>
          <div class="modal-actions fixed-modal-actions">
            <button type="submit" class="rutinas-btn">{{ editandoRutina ? 'Guardar cambios' : 'Crear' }}</button>
            <button type="button" class="rutinas-btn-secundario" @click="cerrarFormulario">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Detalle Rutina -->
    <div v-if="mostrarDetalle" class="modal-bg">
      <div class="modal-form">
        <h3>Detalle de Rutina</h3>
        <div v-if="detalleRutina">
          <p><b>Nombre:</b> {{ detalleRutina.nombre }}</p>
          <p><b>Nivel:</b> {{ detalleRutina.nivel }}</p>
          <p><b>Duración:</b> {{ detalleRutina.duracion }} min</p>
          <div class="tabla" v-if="detalleEjercicios.length">
            <table class="tabla-ejercicios">
              <thead>
                <tr>
                  <th>Ejercicio</th>
                  <th>Reps</th>
                  <th>Series</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ej in detalleEjercicios" :key="ej.id">
                  <td>{{ ej.nombre }}</td>
                  <td>{{ ej.reps }}</td>
                  <td>{{ ej.series }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No hay ejercicios asociados.</p>
          </div>
        </div>
        <div class="modal-actions">
          <button class="rutinas-btn-secundario" @click="cerrarDetalle">Cerrar</button>
        </div>
      </div>
    </div>
    
</template>


<script setup>
import { ref, onMounted } from 'vue'
let temporizadorInterval = null
const temporizadorActivo = ref(false)
const temporizadorRestante = ref(0)
const rutinaTemporizadorId = ref(null)
const temporizadorPausado = ref(false)

function iniciarTemporizador(rutina) {
  if (temporizadorInterval) clearInterval(temporizadorInterval)
  temporizadorRestante.value = rutina.duracion * 60
  rutinaTemporizadorId.value = rutina.id
  temporizadorActivo.value = true
  temporizadorPausado.value = false
  temporizadorInterval = setInterval(() => {
    if (!temporizadorPausado.value && temporizadorRestante.value > 0) {
      temporizadorRestante.value--
      if (temporizadorRestante.value === 0) {
        finalizarTemporizador()
      }
    }
  }, 1000)
}

function pausarTemporizador() {
  temporizadorPausado.value = true
}
function reanudarTemporizador() {
  temporizadorPausado.value = false
}
function reiniciarTemporizador() {
  temporizadorRestante.value = rutinas.value.find(r => r.id === rutinaTemporizadorId.value)?.duracion * 60 || 0
  temporizadorPausado.value = false
}
function finalizarTemporizador() {
  temporizadorActivo.value = false
  rutinaTemporizadorId.value = null
  temporizadorRestante.value = 0
  temporizadorPausado.value = false
  if (temporizadorInterval) clearInterval(temporizadorInterval)
}
function formatoTiempo(segundos) {
  const min = Math.floor(segundos / 60).toString().padStart(2, '0')
  const sec = (segundos % 60).toString().padStart(2, '0')
  return `${min}:${sec}`
}
import api from '../services/api'
import { useAuthStore } from '../store/auth'
const rutinas = ref([])
const cargando = ref(true)
const error = ref(null)
const mostrarFormulario = ref(false)
const mostrarDetalle = ref(false)
const nuevaRutina = ref({ nombre: '', nivel: 'Principiante', duracion: 30, ejercicios: [] })
const ejerciciosSeleccionados = ref([])
const formError = ref('')
const auth = useAuthStore()
const ejerciciosApi = ref([])
const detalleRutina = ref(null)
const detalleEjercicios = ref([])
const editandoRutina = ref(false)
const rutinaEditId = ref(null)

// Cargar ejercicios desde el backend
const cargarEjercicios = async () => {
  const { data } = await api.get('/ejercicios')
  ejerciciosApi.value = data
}

onMounted(async () => {
  await cargarEjercicios()
  await cargarRutinas()
})

function toggleEjercicio(ejNombre) {
  const idx = ejerciciosSeleccionados.value.findIndex(e => e.nombre === ejNombre)
  if (idx === -1) {
    ejerciciosSeleccionados.value.push({ nombre: ejNombre, reps: 8, series: 3 })
  } else {
    ejerciciosSeleccionados.value.splice(idx, 1)
  }
}

function cambiarReps(ejNombre, delta) {
  const ej = ejerciciosSeleccionados.value.find(e => e.nombre === ejNombre)
  if (ej) {
    ej.reps = Math.max(1, ej.reps + delta)
  }
}
function cambiarSeries(ejNombre, delta) {
  const ej = ejerciciosSeleccionados.value.find(e => e.nombre === ejNombre)
  if (ej) {
    ej.series = Math.max(1, ej.series + delta)
  }
}

const cargarRutinas = async () => {
  cargando.value = true
  try {
    const { data } = await api.get('/rutinas/personales')
    rutinas.value = data
    error.value = ''
  } catch (e) {
    error.value = 'No se pudieron cargar las rutinas.'
  } finally {
    cargando.value = false
  }
}

const crearRutina = async () => {
  formError.value = ''
  try {
    const payload = {
      nombre: nuevaRutina.value.nombre,
      nivel: nuevaRutina.value.nivel,
      duracion: nuevaRutina.value.duracion,
      usuario_id: auth.user?.id
    }
    // Crear rutina y obtener su id
    const { data: rutinaCreada } = await api.post('/rutinas', payload)
    // Mapear ejercicios seleccionados a sus ids
    for (const ej of ejerciciosSeleccionados.value) {
      const ejercicioDb = ejerciciosApi.value.find(e => e.nombre === ej.nombre)
      if (ejercicioDb && rutinaCreada.id) {
        await api.post('/rutina_ejercicios', {
          rutina_id: rutinaCreada.id,
          ejercicio_id: ejercicioDb.id,
          reps: ej.reps,
          series: ej.series
        })
      }
    }
    mostrarFormulario.value = false
    nuevaRutina.value = { nombre: '', nivel: 'Principiante', duracion: 30, ejercicios: [] }
    ejerciciosSeleccionados.value = []
    await cargarRutinas()
  } catch (e) {
    formError.value = 'No se pudo crear la rutina.'
  }
}

async function verDetalleRutina(rutina) {
  detalleRutina.value = rutina
  mostrarDetalle.value = true
  // Obtener ejercicios asociados a la rutina
  try {
    // Obtener todos los rutina_ejercicios de esta rutina
    const { data: rutinaEjercicios } = await api.get(`/rutina_ejercicios/`)
    // Filtrar por rutina_id
    const ejerciciosDeRutina = rutinaEjercicios.filter(e => e.rutina_id === rutina.id)
    // Mapear a nombre, reps, series
    // Obtener info de ejercicios
    const { data: ejerciciosDb } = await api.get('/ejercicios')
    detalleEjercicios.value = ejerciciosDeRutina.map(ej => {
      const ejercicio = ejerciciosDb.find(edb => edb.id === ej.ejercicio_id)
      return {
        id: ej.id,
        nombre: ejercicio ? ejercicio.nombre : 'Ejercicio',
        reps: ej.reps,
        series: ej.series
      }
    })
  } catch (e) {
    detalleEjercicios.value = []
  }
}

function cerrarDetalle() {
  mostrarDetalle.value = false
  detalleRutina.value = null
  detalleEjercicios.value = []
}

const cerrarFormulario = () => {
  mostrarFormulario.value = false
  formError.value = ''
}

function abrirEditarRutina(rutina) {
  editandoRutina.value = true
  rutinaEditId.value = rutina.id
  mostrarFormulario.value = true
  nuevaRutina.value = {
    nombre: rutina.nombre,
    nivel: rutina.nivel,
    duracion: rutina.duracion,
    ejercicios: [],
  }
  // Cargar ejercicios seleccionados de la rutina actual
  cargarEjerciciosRutina(rutina.id)
}

async function cargarEjerciciosRutina(rutinaId) {
  // Obtener todos los rutina_ejercicios de esta rutina
  const { data: rutinaEjercicios } = await api.get('/rutina_ejercicios/')
  const ejerciciosDeRutina = rutinaEjercicios.filter(e => e.rutina_id === rutinaId)
  // Obtener info de ejercicios
  const { data: ejerciciosDb } = await api.get('/ejercicios')
  ejerciciosSeleccionados.value = ejerciciosDeRutina.map(ej => {
    const ejercicio = ejerciciosDb.find(edb => edb.id === ej.ejercicio_id)
    return {
      nombre: ejercicio ? ejercicio.nombre : 'Ejercicio',
      reps: ej.reps,
      series: ej.series
    }
  })
}

async function guardarEdicionRutina() {
  formError.value = ''
  try {
    // Actualizar rutina principal
    await api.put(`/rutinas/${rutinaEditId.value}`, {
      nombre: nuevaRutina.value.nombre,
      nivel: nuevaRutina.value.nivel,
      duracion: nuevaRutina.value.duracion,
      usuario_id: auth.user?.id
    })
    // Eliminar todos los rutina_ejercicios actuales de la rutina
    const { data: rutinaEjercicios } = await api.get('/rutina_ejercicios/')
    const ejerciciosDeRutina = rutinaEjercicios.filter(e => e.rutina_id === rutinaEditId.value)
    for (const ej of ejerciciosDeRutina) {
      await api.delete(`/rutina_ejercicios/${ej.id}`)
    }
    // Volver a crear los rutina_ejercicios con los nuevos datos
    for (const ej of ejerciciosSeleccionados.value) {
      const ejercicioDb = ejerciciosApi.value.find(e => e.nombre === ej.nombre)
      if (ejercicioDb) {
        await api.post('/rutina_ejercicios', {
          rutina_id: rutinaEditId.value,
          ejercicio_id: ejercicioDb.id,
          reps: ej.reps,
          series: ej.series
        })
      }
    }
    mostrarFormulario.value = false
    editandoRutina.value = false
    rutinaEditId.value = null
    nuevaRutina.value = { nombre: '', nivel: 'Principiante', duracion: 30, ejercicios: [] }
    ejerciciosSeleccionados.value = []
    await cargarRutinas()
  } catch (e) {
    formError.value = 'No se pudo editar la rutina.'
  }
}

async function eliminarRutina(rutinaId) {
  if (!confirm('¿Seguro que deseas eliminar esta rutina?')) return
  try {
    await api.delete(`/rutinas/${rutinaId}`)
    await cargarRutinas()
  } catch (e) {
    alert('No se pudo eliminar la rutina.')
  }
}
</script>

<style scoped>
.rutina-timer-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.5rem;
}
.rutina-timer-label {
  color: #32be16;
  font-weight: bold;
}
  .rutinas-dashboard-hero {
    width: 100%;
    min-height: 320px;
    background: url('/rutinasFondo.jpg');
    background-size: cover;
    background-position: center center;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .timer-play-btn {
  background: #e6fbe6;
  color: #32be16;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.18s;
}
.timer-play-btn:hover {
  background: #d2f5d2;
}
.timer-box {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.7rem;
  background: #f4f6fa;
  border-radius: 10px;
  padding: 0.5rem 1.1rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.07);
}
.timer-tiempo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #32be16;
  letter-spacing: 1px;
  min-width: 70px;
  text-align: center;
}
.timer-control-btn {
  background: #fff;
  color: #228c0f;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.18s;
}
.timer-control-btn:hover {
  background: #e6fbe6;
}
  .rutinas-hero-overlay {
    width: 100%;
    min-height: 220px;
    background: rgba(34, 44, 68, 0.304);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .rutinas-hero-content {
    text-align: center;
    color: #fff;
    padding: 2.5rem 1.5rem 2rem 1.5rem;
  }
  .rutinas-hero-title {
    font-size: 2.2rem;
    font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
    font-weight: bold;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
    color: #fff;
  }
  .rutinas-hero-subtitle {
    font-size: 1.1rem;
    font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
    font-weight: 400;
    margin-bottom: 1.2rem;
    color: #fff;
  }
  @media (max-width: 700px) {
    .rutinas-dashboard-hero {
      min-height: 180px;
    }
    .rutinas-hero-title {
      font-size: 1.4rem;
    }
    .rutinas-hero-content {
      padding: 1.2rem 0.5rem 1rem 0.5rem;
    }
  }
.rutinas-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.rutinas-btn {
  background: #32be16;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.5rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.rutinas-btn:hover {
  background: #228c0f;
}
.rutinas-wrapper {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  overflow-x: unset;
  overflow-y: unset;
  padding: 1rem;
  scroll-snap-type: none;
}
.tarjeta {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(67,176,42,0.08);
  padding: 1.2rem 1.2rem 1.5rem 1.2rem;
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex: 0 0 auto;
  scroll-snap-align: start;
}
@media (max-width: 700px) {
  .rutinas-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    overflow-x: unset;
    overflow-y: unset;
    padding: 1rem 0.5rem;
    scroll-snap-type: none;
  }
  .tarjeta {
    width: 90vw;
    max-width: 340px;
    margin-left: auto;
    margin-right: auto;
    align-items: center;
    scroll-snap-align: none;
  }
}

.rutina-actions {
  display: flex;
  gap: 0.5rem;
}
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.2rem;
}
.rutinas-btn-secundario {
  background: #112848;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.1rem;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0.7rem;
  cursor: pointer;
  transition: background 0.2s;
}
.rutinas-btn-secundario:hover {
  background: #0a1830;
}
.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-form {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 16px rgba(67,176,42,0.12);
  padding: 2rem 2.5rem;
  min-width: 320px;
  max-width: 95vw;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.modal-form h3 {
  margin-bottom: 0.5rem;
}
.modal-form label {
  font-weight: 600;
  margin-bottom: 0.2rem;
}
.modal-form input, .modal-form select {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #43B02A;
  font-size: 1rem;
  background: #fff;
}
.ejercicios-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1.5rem;
  margin-bottom: 1rem;
}
.ejercicio-checkbox {
  display: flex;
  align-items: center;
  color: #32be16;
}
.ej-nivel {
  color: #888;
  font-size: 0.95em;
  margin-left: 0.3em;
}
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}
.form-error {
  color: #dc2626;
  font-size: 1rem;
  margin-top: 0.5rem;
}
.tabla{
  display: flex;
  align-items: center;
  justify-content: center;
}
.tabla-ejercicios {
  margin: 1rem 0;
  max-height: 260px;
  overflow-y: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(67,176,42,0.08);
  align-self: flex-start;
}
.tabla-ejercicios table {
  width: 100%;
  border-collapse: collapse;

}
.tabla-ejercicios th, .tabla-ejercicios td {
  border: 1px solid #d1d5db;
  padding: 0.5rem 0.7rem;
  text-align: center;
  background: #32be16;
  border-radius: 5px;
  color: #fff;
}
.contador {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2.2em;
  height: 2.2em;
  text-align: center;
  font-weight: 600;
  font-size: 1.1em;
}

.control-flex {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.2em;
}
@media (max-width: 600px) {
  .contador {
    min-width: 1.7em;
    height: 1.7em;
    font-size: 1em;
  }
  .control-flex {
    gap: 0.1em;
  }
}
.tabla-ejercicios button {
  background: #e5e7eb;
  border: none;
  border-radius: 50%;
  width: 2.2em;
  height: 2.2em;
  font-size: 1.3em;
  margin: 0 0.2em;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  padding: 0;
}
.tabla-ejercicios button:hover {
  background: #b6e3b6;
}
/* --- MODAL RESPONSIVE PARA CREAR RUTINA --- */
.responsive-modal {
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
}
.modal-form-content {
  overflow-y: auto;
  flex: 1 1 auto;
  padding-bottom: 1.5rem; /* espacio para los botones fijos */
}
.fixed-modal-actions {
  position: sticky;
  bottom: 0;
  left: 0;
  background: #fff;
  z-index: 10;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  box-shadow: 0 -2px 8px rgba(67,176,42,0.08);
  display: flex;
  gap: 1rem;
  justify-content: center;
}



@media (max-width: 600px) {
  .responsive-modal {
    max-width: 99vw;
    min-width: unset;
    padding: 1rem 0.5rem;
  }
  .modal-form-content {
    font-size: 0.98em;
    padding-bottom: 2.5rem;
  }
  .fixed-modal-actions {
    padding-bottom: 1.2rem;
  }
  .tabla-ejercicios button {
  background: #e5e7eb;
  border: none;
  border-radius: 50%;
  width: 2em;
  height: 2em;
  font-size: 1.1em;
  margin: 0 0.2em;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 5px;
}
.tabla-ejercicios th, .tabla-ejercicios td {
  border: 1px solid #d1d5db;
  padding: 0.5rem 0.7rem;
  text-align: left;
  background: #32be16;
  border-radius: 5px;
  color: #fff;
}
.rutinas-hero-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background: #224da21e;
  position: relative;
  overflow: hidden;
}
.rutinas-hero-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: url('/rutinasFondo.jpg') center center/cover no-repeat;
  opacity: 0.70;
  z-index: 0;
  pointer-events: none;
}
.rutinas-hero-content {
  background: rgba(34, 44, 68, 0.219);
  box-shadow: 0 4px 24px rgba(67,176,42,0.10);
  padding: 2.5rem 2rem;
  width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  position: relative;
  margin-top: 3rem;
  margin-bottom: 2.5rem;
}
.rutinas-hero-logo {
  width: 120px;
  margin-bottom: 1rem;
}
.rutinas-hero-title {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.rutinas-hero-slogan {
  color: #0072BC;
  font-size: 1.08rem;
  margin-bottom: 1.2rem;
  font-weight: 500;
  text-align: center;
}
@media (max-width: 600px) {
  .rutinas-hero-content {
    width: 90vw;
    max-width: 98vw;
    margin: 6vw 2vw 6vw 2vw;
    padding: 1.5rem 0.7rem;
    border-radius: 14px;
  }
  .rutinas-hero-logo {
    width: 80px;
  }
}
@media (max-width: 700px) {
  .rutina-card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }
  .rutina-card-header h3 {
    width: 100%;
    margin-bottom: 0.2rem;
  }
  .rutina-actions {
    width: 100%;
    justify-content: center;
  }
  .icon-btn{
    color: rgba(15, 14, 14, 0.881);
  }
}
}
</style>


