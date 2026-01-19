import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import InicioView from '../views/InicioView.vue'
import PerfilView from '../views/PerfilView.vue'
import RutinasView from '../views/RutinasView.vue'
import ProgresoView from '../views/ProgresoView.vue'
import ParquesView from '../views/ParquesView.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import RegistroView from '../views/RegistroView.vue'
import { useAuthStore } from '../store/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'inicio', component: InicioView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/registro', name: 'registro', component: RegistroView },
    { path: '/perfil', name: 'perfil', component: PerfilView },
    { path: '/rutinas', name: 'rutinas', component: RutinasView },
    { path: '/progreso', name: 'progreso', component: ProgresoView },
    { path: '/parques', name: 'parques', component: ParquesView },
    { path: '/usuario', name: 'usuario', component: UserDashboard },
    { path: '/admin', name: 'admin', component: AdminDashboard }
  ]
})

// Guard de rutas según rol
router.beforeEach((to) => {
  const auth = useAuthStore()
  const publicPages = ['inicio', 'login', 'registro']
  if (!auth.isAuthenticated && !publicPages.includes(to.name)) return { name: 'login' }
  if (to.name === 'admin' && auth.roleId !== 2) return { name: 'usuario' }
})

export default router
