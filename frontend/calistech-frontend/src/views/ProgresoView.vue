
<template>
  <div class="progreso-container">
    <h2>Mi Progreso</h2>
    <div class="progreso-resumen">
      <h3>Resumen mensual</h3>
      <p>Rutinas completadas: <b>12</b></p>
      <p>Días entrenados: <b>18</b></p>
      <p>Mejor marca: <b>Pull-ups: 12</b></p>
    </div>
    <div class="progreso-grafico">
      <!-- Aquí irá un gráfico de progreso (placeholder) -->
      <div class="grafico-placeholder">[Gráfico de barras aquí]</div>
    </div>
    <div class="progreso-logros">
      <h3>Logros recientes</h3>
      <ul>
        <li>🔥 7 días seguidos entrenando</li>
        <li>🏅 10 rutinas completadas</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
// Aquí irá la lógica de progreso
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
</style>
