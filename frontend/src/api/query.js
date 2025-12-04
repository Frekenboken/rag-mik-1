
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // обязательно, чтобы отправлялись httpOnly cookies
  headers: {
    'Content-Type': 'application/json'
  }
})

export const API = {
  getQuery: (request) => api.post('/query', request),
}

export default api
