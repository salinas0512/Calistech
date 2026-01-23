<template>
  <div class="progreso-container">
    <h2>Mi Progreso</h2>
    <div class="progreso-resumen">
      <h3>Resumen mensual</h3>
      <p>Rutinas completadas: <b>{{ rutinasCompletadas }}</b></p>
      <p>Días entrenados: <b>{{ diasEntrenados }}</b></p>
      <p>Mejor marca: <b>{{ mejorMarca }}</b></p>
    </div>
    <div class="progreso-grafico">
      <h3>Gráfico de progreso</h3>
      <canvas ref="graficoRef" width="600" height="220" style="max-width:100%;"></canvas>
    </div>
    <div class="progreso-logros">
      <h3>Logros recientes</h3>
      <ul>
        <li v-for="logro in logros" :key="logro">{{ logro }}</li>
      </ul>
    </div>
    <div class="progreso-nota">
      <h3>Agregar nota de progreso</h3>
      <form @submit.prevent="agregarNota">
        <textarea v-model="nuevaNota" placeholder="Escribe tu nota..." rows="3"></textarea>
        <button type="submit" class="btn-agregar-nota">Guardar nota</button>
      </form>
      <div v-if="mensajeNota" class="mensaje-nota">{{ mensajeNota }}</div>
    </div>
    <div class="progreso-notas-recientes">
      <h3>Notas recientes</h3>
      <ul>
        <li v-for="nota in notasRecientes" :key="nota.id">{{ nota.notas }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const usuarioId = auth.user?.id

const progresos = ref([])
const historial = ref([])
const rutinasCompletadas = ref(0)
const diasEntrenados = ref(0)
const mejorMarca = ref('N/A')
const logros = ref([])
const notasRecientes = ref([])
const nuevaNota = ref('')
const mensajeNota = ref('')
const graficoRef = ref(null)

async function cargarDatos() {
  try {
    const resProgreso = await api.get('/progreso/')
    const resHistorial = await api.get('/historial_progreso/')
    progresos.value = resProgreso.data.filter(p => p.usuario_id === usuarioId)
    historial.value = resHistorial.data.filter(h => h.usuario_id === usuarioId)
    rutinasCompletadas.value = progresos.value.length
    diasEntrenados.value = new Set(historial.value.map(h => h.fecha)).size
    // Mejor marca: ejemplo usando esfuerzo o estadisticas
    mejorMarca.value = calcularMejorMarca()
    logros.value = calcularLogros()
    notasRecientes.value = progresos.value.slice(-5).reverse()
    await nextTick()
    dibujarGrafico()
  } catch (e) {
    rutinasCompletadas.value = 0
    diasEntrenados.value = 0
    mejorMarca.value = 'N/A'
    logros.value = []
    notasRecientes.value = []
  }
}

function calcularMejorMarca() {
  // Ejemplo: buscar el mayor esfuerzo o estadística
  if (progresos.value.length === 0) return 'N/A'
  const maxEsfuerzo = Math.max(...progresos.value.map(p => p.esfuerzo || 0))
  return `Esfuerzo: ${maxEsfuerzo}`
}

function calcularLogros() {
  // Ejemplo: logros por días seguidos y rutinas completadas
  const dias = historial.value.map(h => h.fecha).sort()
  let maxRacha = 1, racha = 1
  for (let i = 1; i < dias.length; i++) {
    const prev = new Date(dias[i - 1])
    const curr = new Date(dias[i])
    if ((curr - prev) / (1000 * 60 * 60 * 24) === 1) {
      racha++
      maxRacha = Math.max(maxRacha, racha)
    } else {
      racha = 1
    }
  }
  const logrosArr = []
  if (maxRacha >= 7) logrosArr.push(`🔥 ${maxRacha} días seguidos entrenando`)
  if (rutinasCompletadas.value >= 10) logrosArr.push(`🏅 ${rutinasCompletadas.value} rutinas completadas`)
  return logrosArr
}

async function agregarNota() {
  if (!nuevaNota.value.trim()) return
  try {
    await api.post('/progreso/', {
      usuario_id: usuarioId,
      rutina: 'Nota rápida',
      duracion: 0,
      esfuerzo: 0,
      notas: nuevaNota.value
    })
    mensajeNota.value = '¡Nota guardada!'
    nuevaNota.value = ''
    await cargarDatos()
  } catch (e) {
    mensajeNota.value = 'Error al guardar la nota.'
  }
  setTimeout(() => mensajeNota.value = '', 2000)
}

function dibujarGrafico() {
  const canvas = graficoRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  // Ejemplo: gráfico de barras de rutinas por día
  const dias = {}
  historial.value.forEach(h => {
    dias[h.fecha] = (dias[h.fecha] || 0) + 1
  })
  const labels = Object.keys(dias).slice(-10)
  const values = Object.values(dias).slice(-10)
  const barWidth = Math.max(30, canvas.width / labels.length - 10)
  for (let i = 0; i < labels.length; i++) {
    const x = 40 + i * (barWidth + 10)
    const y = canvas.height - 30
    const barHeight = values[i] * 18
    ctx.fillStyle = '#32be16'
    ctx.fillRect(x, y - barHeight, barWidth, barHeight)
    ctx.fillStyle = '#222'
    ctx.font = '14px Arial'
    ctx.fillText(labels[i].slice(5), x, canvas.height - 10)
    ctx.fillText(values[i], x + barWidth / 2 - 8, y - barHeight - 8)
  }
}

onMounted(cargarDatos)
</script>

<style scoped>
.progreso-container {
  max-width: 700px;
  margin: 2.5rem auto;
  padding: 0 1.5rem;
}
.progreso-resumen {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(67,176,42,0.08);
  padding: 1.2rem 1.2rem 1.5rem 1.2rem;
  margin-bottom: 2rem;
}
.progreso-grafico {
  background: #f4f6fa;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
  color: #112848;
  font-size: 1.05rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
}
.grafico-placeholder {
  color: #bbb;
  font-size: 1.2rem;
  padding: 2rem 0;
}
.progreso-logros {
  background: #fff;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
}
.progreso-logros ul {
  margin: 0;
  padding-left: 1.2rem;
}
.progreso-nota {
  background: #f4f6fa;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  margin: 2rem 0 1.2rem 0;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
}
.progreso-nota textarea {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.7em 1em;
  font-size: 1rem;
  margin-bottom: 0.7em;
}
.btn-agregar-nota {
  background: #32be16;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7em 1.2em;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.18s;
}
.btn-agregar-nota:hover {
  background: #228c0f;
}
.mensaje-nota {
  color: #32be16;
  margin-top: 0.7em;
}
.progreso-notas-recientes {
  background: #fff;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
  margin-bottom: 2rem;
}
.progreso-notas-recientes ul {
  margin: 0;
  padding-left: 1.2rem;
}
</style>
