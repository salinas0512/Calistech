import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    roleId: Number(localStorage.getItem('roleId')) || null,
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),
  getters: {
    isAuthenticated: (s) => !!s.token
  },
  actions: {
    async login(email, password) {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);
      const { data } = await api.post('/auth/login', params);
      this.token = data.access_token;
      this.roleId = Number(data.role_id);
      this.user = data.user || null;
      localStorage.setItem('token', this.token);
      localStorage.setItem('roleId', this.roleId);
      localStorage.setItem('user', JSON.stringify(this.user));
    },
    logout() {
      this.token = null
      this.roleId = null
      this.user = null
      localStorage.clear()
    }
  }
})
