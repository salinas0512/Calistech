<template>
    <div class="parques-formulario">
      <h3>Registrar nuevo parque</h3>
      <form @submit.prevent="registrarParque">
        <div class="form-row">
          <input v-model="nuevoParque.nombre" type="text" placeholder="Nombre del parque/plaza" required />
          <input v-model="nuevoParque.comuna" type="text" placeholder="Comuna" required />
        </div>
        <div class="form-row">
          <input v-model.number="nuevoParque.lat" type="number" step="any" placeholder="Latitud" required />
          <input v-model.number="nuevoParque.lng" type="number" step="any" placeholder="Longitud" required />
          <button type="button" class="btn-ubicacion" @click="usarUbicacion">Usar mi ubicación</button>
        </div>
        <button type="submit" class="btn-registrar">Registrar parque</button>
      </form>
      <div v-if="mensaje" class="mensaje-parque">{{ mensaje }}</div>
    </div>
  <div class="parques-container">
    <h2>Parques de Calistenia</h2>
    <div class="parques-filtro-row">
      <div class="parques-filtro-input-wrapper" style="margin-bottom: 20px;">
        <input v-model="filtro" type="text" placeholder="Filtrar por nombre o comuna..." 
        style="border-radius: 12px; width: 100%;min-height: 30px; border: 1px solid #43B02A ; background: #fff;"  />
      </div>
    </div>
    <div class="parques-list">
      <!-- Aquí se mostrarán los parques filtrados -->
      <div class="parque-card" v-for="parque in parquesFiltrados" :key="parque.id">
        <h3>{{ parque.nombre }}</h3>
        <p>Comuna: {{ parque.comuna }}</p>
        <p>Latitud: {{ parque.latitud }} | Longitud: {{ parque.longitud }}</p>
        <button class="parques-btn" @click="verEnMapa({ ...parque, lat: parque.latitud, lng: parque.longitud })">Ver en mapa</button>
      </div>
    </div>
    <div class="parques-mapa">
      <Mapa ref="mapaRef" :markers="parquesMarkers" :center="centrarEn || undefined" :key="mapaKey" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import Mapa from '../components/Mapa.vue'
import api from '../services/api'

const parques = ref([])
const filtro = ref("")
const mensaje = ref('')
const mapaRef = ref(null)
const mapaKey = ref(0) // Para forzar el reinicio del mapa si es necesario
const centrarEn = ref(null) // Coordenadas a centrar

// Formulario
const nuevoParque = ref({
  nombre: '',
  comuna: '',
  lat: '',
  lng: ''
})

async function cargarParques() {
  try {
    const res = await api.get('/parques_calisthenia')
    parques.value = res.data
  } catch (e) {
    parques.value = []
  }
}

async function registrarParque() {
  try {
    await api.post('/parques_calisthenia', {
      nombre: nuevoParque.value.nombre,
      comuna: nuevoParque.value.comuna,
      latitud: nuevoParque.value.lat,
      longitud: nuevoParque.value.lng
    })
    mensaje.value = '¡Parque registrado exitosamente!'
    cargarParques()
    // Limpiar formulario
    nuevoParque.value = { nombre: '', comuna: '', lat: '', lng: '' }
    setTimeout(() => mensaje.value = '', 2500)
  } catch (e) {
    mensaje.value = 'Error al registrar parque'
    setTimeout(() => mensaje.value = '', 2500)
  }
}

function usarUbicacion() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      nuevoParque.value.lat = pos.coords.latitude
      nuevoParque.value.lng = pos.coords.longitude
    })
  }
}

const parquesFiltrados = computed(() => {
  if (!filtro.value.trim()) return parques.value;
  const f = filtro.value.trim().toLowerCase();
  return parques.value.filter(p =>
    (p.nombre && p.nombre.toLowerCase().includes(f)) ||
    (p.comuna && p.comuna.toLowerCase().includes(f))
  );
});

const parquesMarkers = computed(() =>
  parquesFiltrados.value
    .filter(p =>
      typeof p.latitud === 'number' &&
      typeof p.longitud === 'number' &&
      !isNaN(p.latitud) &&
      !isNaN(p.longitud)
    )
    .map(p => ({
      lat: p.latitud,
      lng: p.longitud,
      label: p.nombre
    }))
)

function verEnMapa(parque) {
  centrarEn.value = [parque.lat, parque.lng]
  mapaKey.value++ // Forzar actualización si es necesario
  nextTick(() => {
    if (mapaRef.value && mapaRef.value.centrarYPopup) {
      mapaRef.value.centrarYPopup(parque.lat, parque.lng, parque.nombre)
    }
    // Scroll automático al mapa
    const mapaDiv = document.querySelector('.parques-mapa');
    if (mapaDiv) {
      mapaDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  })
}

cargarParques()
</script>

<style scoped>
  .parques-formulario {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(67,176,42,0.08);
    padding: 1.5rem 1.5rem 1.2rem 1.5rem;
    margin-bottom: 2.2rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
  }
  .parques-formulario h3 {
    color: #32be16;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1.1rem;
    text-align: center;
  }
  .form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }
  .form-row input {
    flex: 1 1 150px;
    padding: 0.6rem 0.8rem;
    border: 1px solid #d2e5d2;
    border-radius: 7px;
    font-size: 1rem;
    border: 1px solid #43B02A;
    background: #fff;
  }
  .btn-ubicacion {
    background: #e6fbe6;
    color: #32be16;
    border: none;
    border-radius: 7px;
    padding: 0.6rem 1.1rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.18s;
  }
  .btn-ubicacion:hover {
    background: #d2f5d2;
  }
  .btn-registrar {
    background: #32be16;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0.7rem 2.2rem;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.18s;
    display: block;
    margin: 0 auto;
  }
  .btn-registrar:hover {
    background: #228c0f;
  }
  .mensaje-parque {
    margin-top: 1rem;
    color: #228c0f;
    text-align: center;
    font-weight: 600;
  }
.parques-container {
  max-width: 900px;
  margin: 2.5rem auto;
  padding: 0 1.5rem;
}
.parques-list {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: flex-start;
  margin-bottom: 2rem;
}
.parque-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(67,176,42,0.08);
  padding: 1.2rem 1.2rem 1.5rem 1.2rem;
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

@media (max-width: 700px) {
  .parques-list {
    justify-content: center;
    gap: 1.2rem;
  }
  .parque-card {
    width: 90vw;
    max-width: 340px;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
  }
}
.parques-btn {
  background: #32be16;
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
.parques-btn:hover {
  background: #228c0f;
}
.parques-mapa {
.parques-mapa {
  background: #f4f6fa;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  text-align: center;
  color: #112848;
  font-size: 1.05rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
}
.parques-filtro-row {
  margin-bottom: 1.2rem;
  display: flex;
  justify-content: flex-end;
}
.parques-filtro-input-wrapper i{
  position: relative;
  width: 100%;
  max-width: 350px;
  margin: 0 auto 1.2rem auto;
}
.parques-filtro-input {
  width: 100%;
  padding: 0.7rem 2.2rem 0.7rem 1rem;
  border-radius: 8px;
  border: 2px solid #43B02A ;
  border-radius: 12px;
  font-size: 1.08rem;
  background: #fff;
  box-sizing: border-box;
}

.parques-filtro-input:focus {
  box-shadow: 0 0 0 2px #a5d6a7;
}
.parques-filtro-input::placeholder {
  color: #a5d6a7;
  opacity: 1;
  font-size: 1.01rem;
}
}
.mapa-placeholder {
  color: #bbb;
  font-size: 1.2rem;
  padding: 2rem 0;
}

</style>


