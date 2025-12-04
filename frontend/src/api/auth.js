// src/api/auth.js
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // обязательно, чтобы отправлялись httpOnly cookies
  headers: {
    'Content-Type': 'application/json'
  }
})

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (data) => api.post('/auth/register', data),
  getProfile: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout')
}

export default api
