<template>
  <div class="perfil-container">
    <div class="perfil-card">
      <div class="perfil-avatar-section">
        <img :src="user.fotoPerfil || defaultAvatar" alt="Foto de perfil" class="perfil-avatar" />
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
          <span>{{ user.objetivo || 'No definido' }}</span>
          <button class="perfil-btn perfil-btn-mini" @click="editarObjetivo">Editar</button>
        </div>
        <div class="perfil-nivel">
          <label>Nivel actual:</label>
          <span>{{ user.nivel || 'No definido' }}</span>
        </div>
        <div class="perfil-preferencias">
          <label>Preferencias:</label>
          <span>{{ user.preferencias || 'No definidas' }}</span>
        </div>
      </div>
      <div class="perfil-acciones">
        <button class="perfil-btn" @click="editarPerfil">Editar perfil</button>
        <button class="perfil-btn perfil-btn-secundario" @click="cambiarContrasena">Cambiar contraseña</button>
        <button class="perfil-btn perfil-btn-peligro" @click="eliminarCuenta">Eliminar cuenta</button>
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
import { ref } from 'vue'
const defaultAvatar = '/avatar-default.png'
// Simulación de datos de usuario (reemplazar por datos reales del store o API)
const user = ref({
  fotoPerfil: '',
  nombre: 'Nombre Usuario',
  email: 'usuario@email.com',
  rol: 'Usuario',
  fechaRegistro: '2024-01-01',
  objetivo: 'Mejorar fuerza',
  nivel: 'Intermedio',
  preferencias: 'Mañana, Parque Central, Rutinas Fullbody',
  rutinasMes: 12
})
function cambiarFoto() { /* lógica para subir foto */ }
function editarPerfil() { /* lógica para editar perfil */ }
function cambiarContrasena() { /* lógica para cambiar contraseña */ }
function eliminarCuenta() { /* lógica para eliminar cuenta */ }
function editarObjetivo() { /* lógica para editar objetivo */ }
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
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
.perfil-avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #32be16;
  margin-bottom: 0.7rem;
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
</style>
