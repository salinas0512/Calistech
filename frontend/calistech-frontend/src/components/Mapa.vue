<template>
  <div class="map-wrapper">
    <div id="map" class="map-container"></div>
    <button class="btn-geo" @click="centrarEnMiUbicacion" title="Ir a mi ubicación">
      <i class="fa-solid fa-location-crosshairs"></i>
    </button>
  </div>
</template>

<script setup>
import { onMounted, watch, ref, defineExpose } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Props para marcadores dinámicos
const props = defineProps({
  markers: {
    type: Array,
    default: () => []
  },
  center: {
    type: Array,
    default: () => [-33.45, -70.65] // Santiago por defecto
  },
  zoom: {
    type: Number,
    default: 13
  }
});

const map = ref(null);
const markerLayer = ref(null);
const popupRefs = ref({});
const userMarker = ref(null);

onMounted(() => {
  map.value = L.map('map').setView(props.center, props.zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map.value);

  // Eliminar centrarEnMiUbicacion automático aquí
  // centrarEnMiUbicacion();

  markerLayer.value = L.layerGroup().addTo(map.value);
  updateMarkers();
});

// Actualizar marcadores si cambian
watch(() => props.markers, updateMarkers, { deep: true });

function updateMarkers() {
  if (!markerLayer.value) return;
  markerLayer.value.clearLayers();
  popupRefs.value = {};
  // Icono deportivo/calistenia local
  const parqueIcon = L.icon({
    iconUrl: '/exercise.png', // archivo en public
    iconSize: [42, 42],
    iconAnchor: [18, 36],
  });
  props.markers.forEach(m => {
    const marker = L.marker([m.lat, m.lng], { icon: parqueIcon })
      .addTo(markerLayer.value)
      .bindPopup(m.label || 'Plaza de calistenia');
    popupRefs.value[`${m.lat},${m.lng}`] = marker;
  });
}

function centrarYPopup(lat, lng, label) {
  if (map.value) {
    map.value.setView([lat, lng], 16);
    const key = `${lat},${lng}`;
    if (popupRefs.value[key]) {
      popupRefs.value[key].openPopup();
    }
  }
}

defineExpose({ centrarYPopup });

function centrarEnMiUbicacion() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      map.value.setView([lat, lon], 15);
      if (userMarker.value) {
        userMarker.value.setLatLng([lat, lon]);
      } else {
        userMarker.value = L.marker([lat, lon], { icon: L.icon({
          iconUrl: 'https://cdn-icons-png.flaticon.com/512/64/64113.png',
          iconSize: [32, 32],
          iconAnchor: [16, 32],
        }) })
          .addTo(map.value)
          .bindPopup('Tu ubicación actual');
      }
      userMarker.value.openPopup();
    });
  }
}
</script>

<style scoped>
.map-wrapper {
  position: relative;
}
.map-container {
  width: 100%;
  height: 400px;
  border-radius: 14px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.10);
  margin: 0 auto;
  z-index: 1;
}
.btn-geo {
  position: absolute;
  bottom: 18px;
  right: 18px;
  background: #fff;
  color: #32be16;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  box-shadow: 0 2px 8px rgba(67,176,42,0.13);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.18s;
  z-index: 10;
}
.btn-geo:hover {
  background: #e6fbe6;
}
</style>
