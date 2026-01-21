<template>
  <div class="dashboard-hero">
    <div class="hero-overlay">
      <div class="hero-content">
        <h1 class="hero-title">¡Bienvenido {{ username }}!</h1>
        <p class="hero-subtitle">Sigue avanzando en tu camino calisténico.</p>
      </div>
    </div>
  </div>
  <div class="dashboard-main">
    <!-- Rutinas recomendadas por nivel (horizontal) -->
    <div class="rutinas-nivel-section">
      <h2 class="rutinas-nivel-title">Rutinas recomendadas según nivel</h2>
      <div class="rutinas-nivel-list-horizontal">
        <div v-for="rutina in rutinas" :key="rutina.nivel" class="rutina-card-horizontal">
          <h3 class="rutina-nivel">{{ rutina.nivel }}</h3>
          <div class="rutina-video-wrapper-horizontal">
            <!-- Previsualización de video de YouTube -->
            <iframe
              :src="rutina.videoUrl"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              class="rutina-video"
            ></iframe>
          </div>
          <p class="rutina-desc">{{ rutina.descripcion }}</p>
          <a :href="rutina.linkYoutube" target="_blank" class="ver-en-youtube">Ver en YouTube</a>
        </div>
      </div>
    </div>
    <!-- Carrusel de tips motivacionales -->
    <div class="dashboard-tips-glass" @touchstart="onTouchStart" @touchend="onTouchEnd">
      <h3 class="tips-title">
        <svg width="22" height="22" fill="none" viewBox="0 0 24 24" class="tips-icon"><path d="M12 2C6.48 2 2 6.48 2 12c0 4.41 3.59 8 8 8s8-3.59 8-8c0-5.52-4.48-10-8-10zm0 18c-4.41 0-8-3.59-8-8 0-4.41 3.59-8 8-8s8 3.59 8 8c0 4.41-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#32be16"/></svg>
        Frases para motivarte
      </h3>
      <transition name="fade" mode="out-in">
        <blockquote :key="currentTipIndex" class="tips-quote">{{ tips[currentTipIndex].texto }}</blockquote>
      </transition>
      <div class="tips-controls-glass">
        <button @click="prevTip" class="tips-btn-glass" aria-label="Anterior">
          <i class="fa-solid fa-caret-left"></i>
        </button>
        <span class="tips-indicator-glass">{{ currentTipIndex + 1 }} / {{ tips.length }}</span>
        <button @click="nextTip" class="tips-btn-glass" aria-label="Siguiente">
          <i class="fa-solid fa-caret-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
const auth = useAuthStore()
const username = auth.user?.nombre || 'Usuario'

// Tips motivacionales (top 10)
const tips = [
  { texto: "Ningún ciudadano tiene derecho a ser un aficionado en el entrenamiento físico. Qué desgracia es para un hombre crecer sin ver la belleza y fuerza de lo que su cuerpo es capaz. — Sócrates" },
  { texto: "Vamos a conseguir muchas más cosas si pensamos que nada es imposible. Ahuyenta los pensamientos negativos y sigue adelante. — Vince Lombardi" },
  { texto: "Mantener nuestro cuerpo con buena salud es un deber. De lo contrario no seremos capaces de mantener nuestras mentes fuertes y claras. — Buddha" },
  { texto: "Odié cada minuto de entrenamiento, pero dije, “no te rindas. Sufre ahora y vive el resto de tu vida como un campeón”. — Muhammad Ali" },
  { texto: "La fuerza no viene de una capacidad física. Viene de una voluntad indomable. — Mahatma Gandhi" },
  { texto: "El camino a ninguna parte está pavimentado con excusas. — Mark Bell" },
  { texto: "El primer paso es el más importante. Es el más crucial y más efectivo, ya que iniciará la dirección que has elegido. — Steve Backley" },
  { texto: "Cada paso que das es un paso alejado de donde solías estar. Permítete un bajón, pero no dos. — Brian Chargualaf" },
  { texto: "Siempre parece imposible hasta que se hace. — Nelson Mandela" },
  { texto: "No puedes poner un límite a nada. Cuanto más sueñas, más lejos llegas. — Michael Phelps" }
]

// Estado del carrusel
const currentTipIndex = ref(0)

function nextTip() {
  currentTipIndex.value = (currentTipIndex.value + 1) % tips.length
}
function prevTip() {
  currentTipIndex.value = (currentTipIndex.value - 1 + tips.length) % tips.length
}

// Swipe para móviles
let touchStartX = 0
function onTouchStart(e) {
  touchStartX = e.changedTouches[0].screenX
}
function onTouchEnd(e) {
  const touchEndX = e.changedTouches[0].screenX
  if (touchEndX - touchStartX > 40) prevTip()
  else if (touchStartX - touchEndX > 40) nextTip()
}

// Rutinas recomendadas por nivel
const rutinas = [
  {
    nivel: 'Principiante',
    descripcion: 'Rutina básica para quienes recién comienzan en la calistenia. Ejercicios sencillos y explicados paso a paso.',
    videoUrl: 'https://www.youtube.com/embed/AUK6QIhSWhs', 
    linkYoutube: 'https://www.youtube.com/watch?v=AUK6QIhSWhs'
  },
  {
    nivel: 'Intermedio',
    descripcion: 'Rutina intermedia para quienes ya dominan lo básico y buscan nuevos desafíos.',
    videoUrl: 'https://www.youtube.com/embed/rOhqwjcVwLI',
    linkYoutube: 'https://www.youtube.com/watch?v=rOhqwjcVwLI'
  },
  {
    nivel: 'Avanzado',
    descripcion: 'Rutina avanzada para quienes buscan llevar su cuerpo y habilidades al siguiente nivel.',
    videoUrl: 'https://www.youtube.com/embed/3p8EBPVZ2Iw',
    linkYoutube: 'https://www.youtube.com/watch?v=3p8EBPVZ2Iw'
  }
]
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
.dashboard-hero {
  width: 100%;
  min-height: 450px;
  background: url('/calistechf2.jpg');
  background-size: cover;
  background-position: left center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 50%;
  transform: translateX(-50%);
  left: 0;

}
.hero-overlay {
  width: 100%;
  min-height: 240px;
  background: rgba(34, 44, 68, 0.45);
  backdrop-filter: blur(2.5px);
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-content {
  text-align: center;
  color: #fff;
  padding: 2.5rem 1.5rem 2rem 1.5rem;
}
.hero-title {
  font-size: 2.5rem;
  font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
  font-weight: bold;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}
.hero-subtitle {
  font-size: 1.2rem;
  font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
  font-weight: 400;
  margin-bottom: 0;
}
.dashboard-main {
  max-width: 700px;
  margin: 2.5rem auto 0 auto;
  padding: 0 1.5rem;
}
.dashboard-tips-glass {
  background: rgba(255,255,255,0.65);
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(67,176,42,0.10);
  padding: 2rem 2.2rem 1.7rem 2.2rem;
  margin-top: 2.2rem;
  text-align: center;
  color: #112848;
  font-size: 1.13rem;
  box-shadow: 0 2px 8px rgba(67,176,42,0.08);
  position: relative;
  min-height: 140px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  backdrop-filter: blur(7px);
  border: 1.5px solid rgba(50,190,22,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.tips-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #32be16;
  font-size: 1.25rem;
  font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
  margin-bottom: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.2px;
}
.tips-icon {
  vertical-align: middle;
}
.tips-quote {
  font-style: italic;
  color: #112848;
  font-size: 1.13rem;
  margin: 0 0 0.7rem 0;
  min-height: 60px;
  transition: color 0.2s;
  line-height: 1.5;
  letter-spacing: 0.1px;
}
.tips-controls-glass {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  margin-top: 0.7rem;
  background: rgba(255,255,255,0.45);
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(67,176,42,0.06);
  padding: 0.3rem 1.1rem;
}
.tips-btn-glass {
  background: #32be16;
  border: none;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  outline: none;
  color: #fff;
  box-shadow: 0 2px 8px rgba(67,176,42,0.10);
}
.tips-btn-glass:hover {
  background: #228c0f;
  color: #fff;
}
.tips-btn-glass i {
  font-size: 1.7rem;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tips-btn-glass svg path {
  fill: #fff;
  transition: fill 0.2s;
}
.tips-btn-glass:hover svg path {
  fill: #fff;
}
.tips-indicator-glass {
  color: #32be16;
  font-weight: 600;
  font-size: 1.08rem;
  letter-spacing: 0.2px;
  background: rgba(255,255,255,0.7);
  border-radius: 8px;
  padding: 0.2rem 1.1rem;
  box-shadow: 0 1px 4px rgba(67,176,42,0.04);
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s cubic-bezier(.4,0,.2,1);
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.rutinas-nivel-section {
  margin: 2.5rem 0 2rem 0;
}
.rutinas-nivel-title {
  text-align: center;
  color: #32be16;
  font-size: 1.5rem;
  font-family: 'Montserrat', 'Poppins', Arial, sans-serif;
  margin-bottom: 1.5rem;
}
.rutinas-nivel-list-horizontal {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  justify-content: space-between;
  align-items: stretch;
  width: 100%;
  padding-bottom: 1rem;
  scrollbar-width: thin;
  scrollbar-color: #32be16 #f4f6fa;
}
.rutina-card-horizontal {
  background: rgba(255,255,255,0.97);
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(67,176,42,0.08);
  padding: 1.2rem 1.2rem 1.5rem 1.2rem;
  flex: 1 1 0;
  min-width: 0;
  max-width: 340px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}
.rutina-video-wrapper-horizontal {
  width: 100%;
  aspect-ratio: 16/9;
  margin-bottom: 0.7rem;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(67,176,42,0.10);
}
.rutina-nivel {
  color: #112848;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.7rem;
}
.rutina-video {
  width: 100%;
  height: 100%;
  border: none;
}
.rutina-desc {
  color: #555A60;
  font-size: 1rem;
  margin: 0.7rem 0 0.5rem 0;
  text-align: center;
}
.ver-en-youtube {
  color: #32be16;
  font-weight: 600;
  text-decoration: underline;
  font-size: 1.05rem;
  margin-top: 0.2rem;
  transition: color 0.2s;
}
.ver-en-youtube:hover {
  color: #228c0f;
}
@media (max-width: 900px) {
  .rutinas-nivel-list-horizontal {
    gap: 1rem;
  }
  .rutina-card-horizontal {
    max-width: 260px;
    padding: 0.7rem 0.7rem 1rem 0.7rem;
  }
}
@media (max-width: 700px) {
  .rutinas-nivel-list-horizontal {
    flex-direction: column;
    gap: 1.2rem;
  }
  .rutina-card-horizontal {
    max-width: 100%;
    width: 100%;
    min-width: 0;
  }
}
</style>
