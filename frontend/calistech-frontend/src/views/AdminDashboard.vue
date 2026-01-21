<template>
  <div class="admin-dashboard">
    <h2 class="admin-title">Panel de Administrador</h2>
    <div class="admin-summary">
      <div class="admin-card users">
        <div class="admin-card-icon"><i class="fa-solid fa-users"></i></div>
        <div class="admin-card-content">
          <span class="admin-card-label">Usuarios</span>
          <span class="admin-card-value">{{ usersCount }}</span>
          <button class="admin-card-view-btn" @click="openUsers">Ver todos</button>
        </div>
      </div>
      <div class="admin-card routines">
        <div class="admin-card-icon"><i class="fa-solid fa-dumbbell"></i></div>
        <div class="admin-card-content">
          <span class="admin-card-label">Rutinas</span>
          <span class="admin-card-value">{{ routinesCount }}</span>
          <button class="admin-card-view-btn" @click="openRoutines">Ver todas</button>
        </div>
      </div>
      <div class="admin-card parks">
        <div class="admin-card-icon"><i class="fa-solid fa-tree"></i></div>
        <div class="admin-card-content">
          <span class="admin-card-label">Parques</span>
          <span class="admin-card-value">{{ parksCount }}</span>
          <button class="admin-card-view-btn" @click="openParks">Ver todos</button>
        </div>
      </div>
    </div>

    <!-- Modales visuales para mostrar listas -->
    <div v-if="showUsers" class="admin-modal-bg" @click.self="showUsers = false">
      <div class="admin-modal">
        <h3>Lista de usuarios</h3>
        <ul class="admin-list">
          <li v-for="user in users" :key="user.id || user._id">
            <b>{{ user.username || user.nombre_usuario }}</b>
            <span v-if="user.email">  {{ user.email }}</span>
          </li>
        </ul>
        <button class="admin-modal-close" @click="showUsers = false">Cerrar</button>
      </div>
    </div>
    <div v-if="showRoutines" class="admin-modal-bg" @click.self="showRoutines = false">
      <div class="admin-modal">
        <h3>Lista de rutinas</h3>
        <ul class="admin-list">
          <li v-for="routine in routines" :key="routine.id || routine._id">
            <b>{{ routine.name || routine.nombre }}</b>
            <span v-if="routine.level || routine.nivel"> - {{ routine.level || routine.nivel }}</span>
          </li>
        </ul>
        <button class="admin-modal-close" @click="showRoutines = false">Cerrar</button>
      </div>
    </div>
    <div v-if="showParks" class="admin-modal-bg" @click.self="showParks = false">
      <div class="admin-modal">
        <h3>Lista de parques</h3>
        <ul class="admin-list">
          <li v-for="park in parks" :key="park.id || park._id">
            <b>{{ park.name || park.nombre }}</b>
            <span v-if="park.location || park.ubicacion"> - {{ park.location || park.ubicacion }}</span>
          </li>
        </ul>
        <button class="admin-modal-close" @click="showParks = false">Cerrar</button>
      </div>
    </div>
    <div class="admin-actions">
      <button class="admin-action-btn"><i class="fa-solid fa-user-gear"></i> Gestionar usuarios</button>
      <button class="admin-action-btn"><i class="fa-solid fa-dumbbell"></i> Gestionar rutinas</button>
      <button class="admin-action-btn"><i class="fa-solid fa-tree"></i> Gestionar parques</button>
    </div>
    <div class="admin-reports">
      <h3 class="admin-reports-title">Reportes recientes</h3>
      <ul class="admin-reports-list">
        <li><span class="report-date">21/01/2026</span> Usuario <b>juanperez</b> reportó un error en rutina "Full Body"</li>
        <li><span class="report-date">20/01/2026</span> Nuevo parque registrado: <b>Parque Central</b></li>
        <li><span class="report-date">19/01/2026</span> Usuario <b>mariafit</b> completó 30 rutinas</li>
        <li><span class="report-date">18/01/2026</span> Se eliminó la cuenta de <b>usuario123</b></li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
// Estados para mostrar modales
const showUsers = ref(false);
const showRoutines = ref(false);
const showParks = ref(false);
// Datos reales
const users = ref([]);
const routines = ref([]);
const parks = ref([]);
const reports = ref([]);
// Contadores para tarjetas
const usersCount = ref(0);
const routinesCount = ref(0);
const parksCount = ref(0);
// Cargar datos al abrir cada modal
async function fetchUsers() {
  try {
    const res = await api.get('/usuarios');
    users.value = res.data;
    usersCount.value = res.data.length;
  } catch (e) {
    users.value = [];
    usersCount.value = 0;
  }
}
async function fetchRoutines() {
  try {
    const res = await api.get('/rutinas');
    routines.value = res.data;
    routinesCount.value = res.data.length;
  } catch (e) {
    routines.value = [];
    routinesCount.value = 0;
  }
}
async function fetchParks() {
  try {
    const res = await api.get('/parques_calisthenia');
    parks.value = res.data;
    parksCount.value = res.data.length;
  } catch (e) {
    parks.value = [];
    parksCount.value = 0;
  }
}
async function fetchReports() {
  try {
    const res = await api.get('/reportes');
    reports.value = res.data;
  } catch (e) {
    reports.value = [];
  }
}
// Cargar contadores y reportes al montar
onMounted(() => {
  fetchUsers();
  fetchRoutines();
  fetchParks();
  fetchReports();
});
// Abrir modal y cargar datos si es necesario
function openUsers() {
  showUsers.value = true;
  fetchUsers();
}
function openRoutines() {
  showRoutines.value = true;
  fetchRoutines();
}
function openParks() {
  showParks.value = true;
  fetchParks();
}
</script>

<style scoped>
  @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
/* Botón para ver todos */
.admin-card-view-btn {
  margin-top: 0.5rem;
  background: #fbeaea;
  color: #dc2626;
  border: none;
  border-radius: 7px;
  padding: 0.35rem 1.1rem;
  font-size: 0.98rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s;
}
.admin-card-view-btn:hover {
  background: #ffeaea;
}
/* Modales visuales */
.admin-modal-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.35); /* Más oscuro para mejor contraste */
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.admin-modal {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 24px rgba(220,38,38,0.18);
  padding: 2rem 2.5rem 1.5rem 2.5rem;
  min-width: 320px;
  max-width: 95vw;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  z-index: 2100;
}
.admin-modal h3 {
  color: #dc2626;
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 1.1rem;
  text-align: center;
}
.admin-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1.2rem 0;
}
.admin-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f2dede;
  color: #333;
  font-size: 1.04rem;
}
.admin-list li:last-child {
  border-bottom: none;
}
.admin-modal-close {
  display: block;
  margin: 1.2rem auto 0 auto;
  background: #dc2626;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2.2rem;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.18s;
}
.admin-modal-close:hover {
  background: #a81d1d;
}

.admin-dashboard {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 1.2rem 2.5rem 1.2rem;
}
.admin-title {
  color: #dc2626;
  font-size: 2.1rem;
  font-weight: 700;
  margin-bottom: 2.2rem;
  text-align: center;
  letter-spacing: 0.5px;
}
.admin-summary {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}
.admin-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(220,38,38,0.08);
  padding: 1.5rem 2.2rem;
  display: flex;
  align-items: center;
  min-width: 210px;
  gap: 1.1rem;
  transition: box-shadow 0.2s;
}
.admin-card:hover {
  box-shadow: 0 4px 24px rgba(220,38,38,0.16);
}
.admin-card-icon {
  font-size: 2.2rem;
  color: #dc2626;
  background: #fbeaea;
  border-radius: 50%;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.admin-card-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.admin-card-label {
  font-size: 1.08rem;
  color: #555A60;
  margin-bottom: 0.2rem;
}
.admin-card-value {
  font-size: 1.7rem;
  font-weight: 700;
  color: #dc2626;
}
.admin-actions {
  display: flex;
  gap: 1.2rem;
  justify-content: center;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}
.admin-action-btn {
  background: #dc2626;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.8rem 1.7rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  box-shadow: 0 2px 8px rgba(220,38,38,0.08);
}
.admin-action-btn:hover {
  background: #a81d1d;
}
.admin-reports {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(220,38,38,0.07);
  padding: 1.5rem 2rem 1.2rem 2rem;
  max-width: 600px;
  margin: 0 auto;
}
.admin-reports-title {
  color: #dc2626;
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1.1rem;
}
.admin-reports-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.admin-reports-list li {
  padding: 0.6rem 0;
  border-bottom: 1px solid #f2dede;
  color: #333;
  font-size: 1.04rem;
}
.admin-reports-list li:last-child {
  border-bottom: none;
}
.report-date {
  color: #dc2626;
  font-weight: 600;
  margin-right: 0.5rem;
}
@media (max-width: 700px) {
  .admin-summary {
    flex-direction: column;
    align-items: center;
    gap: 1.2rem;
  }
  .admin-actions {
    flex-direction: column;
    align-items: center;
    gap: 0.7rem;
  }
}
</style>
