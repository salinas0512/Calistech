
<template>
  <div class="parques-container">
    <h2>Parques de Calistenia</h2>
    <div class="parques-list">
      <!-- Aquí se mostrarán los parques -->
      <div class="parque-card" v-for="parque in parques" :key="parque.id">
        <h3>{{ parque.nombre }}</h3>
        <p>Ubicación: {{ parque.ubicacion }}</p>
        <button class="parques-btn">Ver en mapa</button>
      </div>
    </div>
    <div class="parques-mapa">
      <!-- Aquí irá el mapa (placeholder) -->
      <div class="mapa-placeholder">[Mapa aquí]</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const parques = ref([
  { id: 1, nombre: 'Parque Central', ubicacion: 'Centro' },
  { id: 2, nombre: 'Parque Norte', ubicacion: 'Norte' },
  { id: 3, nombre: 'Parque Sur', ubicacion: 'Sur' }
])
</script>

<style scoped>
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
  background: #f4f6fa;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  text-align: center;
  color: #112848;
  font-size: 1.05rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.04);
}
.mapa-placeholder {
  color: #bbb;
  font-size: 1.2rem;
  padding: 2rem 0;
}
</style>
