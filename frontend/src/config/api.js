// src/config/api.js
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/auth/login',
      REGISTER: '/auth/register',
      LOGOUT: '/auth/logout'
    },
    // USERS: {
    //   PROFILE: '/users/profile',
    //   UPDATE: '/users/update',
    //   AVATAR: '/users/avatar'
    // },
    LLM: {
      QUERY: '/query',
    }
  }
}

// Получение полного URL
export const getApiUrl = (endpoint) => `${API_CONFIG.BASE_URL}${endpoint}`