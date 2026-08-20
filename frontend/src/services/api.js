/**
 * services/api.js — Axios instance with JWT auth and auto-logout on 401
 */
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

export const authService = {
  async login(email, password) {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    const { data } = await api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return data;
  },

  async register(fullName, email, password) {
    const { data } = await api.post('/auth/register', {
      full_name: fullName,
      email,
      password,
    });
    return data;
  },

  async getMe() {
    const { data } = await api.get('/auth/me');
    return data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },
};

export const projectService = {
  async getAll() {
    const { data } = await api.get('/projects');
    return data;
  },

  async getById(id) {
    const { data } = await api.get(`/projects/${id}`);
    return data;
  },

  async create(payload) {
    const { data } = await api.post('/projects', payload);
    return data;
  },

  async update(id, payload) {
    const { data } = await api.put(`/projects/${id}`, payload);
    return data;
  },

  async delete(id) {
    await api.delete(`/projects/${id}`);
  },
};
