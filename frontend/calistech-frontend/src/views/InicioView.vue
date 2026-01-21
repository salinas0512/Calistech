<template>
  <div class="inicio-container">
    <div class="inicio-bg-full"></div>
    <div class="inicio-content">
      <img src="/logo500.png" alt="Logo CalisTech" class="inicio-logo" />
      <h1 class="inicio-title">Bienvenido a CalisTech</h1>
      <h2 class="inicio-slogan">¡Progreso, disciplina y salud en tus manos!</h2>
      <p class="inicio-desc">
        CalisTech es la plataforma integral para entusiastas de la calistenia. Descubre rutinas, registra tu avance, encuentra parques y accede a herramientas exclusivas para tu progreso físico.
      </p>
      <div class="inicio-actions">
        <router-link to="/login" class="inicio-btn login">Iniciar sesión</router-link>
        <router-link to="/registro" class="inicio-btn register">Registrarse</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// No requiere lógica especial
</script>

<style scoped>
.inicio-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6fa;
  position: relative;
  overflow: hidden;
}
.inicio-bg-full {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: url('/calistechf3.jpg') center center/cover no-repeat;
    opacity: 0.70;
  z-index: 0;
  pointer-events: none;
}
.inicio-content {
  background: rgba(255,255,255,0.85); /* overlay semitransparente solo al formulario */
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(67,176,42,0.10);
  padding: 2.5rem 2rem;
  width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  position: relative;
}
.inicio-logo {
  width: 140px;
  margin-bottom: 1rem;
}
.inicio-title {
  color: #43B02A;
  font-size: 2.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.inicio-slogan {
  color: #0072BC;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  font-weight: 500;
  text-align: center;
}
.inicio-desc {
  color: #555A60;
  font-size: 1rem;
  margin-bottom: 2rem;
  text-align: center;
}
.inicio-actions {
  display: flex;
  gap: 1rem;
}
.inicio-btn {
  background: #43B02A;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.7rem 1.2rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.2s;
}
.inicio-btn.login {
  background: #43B02A;
}
.inicio-btn.register {
  background: #0072BC;
}
.inicio-btn:hover {
  opacity: 0.85;
}

/*media querys*/

@media (max-width: 600px) {
  .inicio-content {
    width: 85vw;
    max-width: 98vw;
    margin: 6vw 2vw 6vw 2vw;
    padding: 1.5rem 0.7rem;
    border-radius: 14px;
  }
}

</style>
