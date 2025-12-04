// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const initialized = ref(false)

  const login = async (credentials) => {
    try {
      await authAPI.login(credentials)
      const profile = await authAPI.getProfile()
      user.value = profile.data
      initialized.value = true
    } catch (err) {
      initialized.value = true
      throw err
    }
  }

  const register = async (data) => {
    try {
      await authAPI.register(data)
      const profile = await authAPI.getProfile()
      user.value = profile.data
      initialized.value = true
    } catch (err) {
      initialized.value = true
      throw err
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()  // делаем запрос на сервер
      user.value = null        // только если сервер ответил успешно
      return true
    } catch (err) {
      console.error('Ошибка при logout:', err)
      return false             // сервер не ответил → пользователь остаётся в системе
    }
  }



  const checkAuth = async () => {
    try {
      const profile = await authAPI.getProfile()
      user.value = profile.data
    } catch {
      user.value = null
    } finally {
      initialized.value = true
    }
  }

  return {
    user,
    isAuthenticated,
    initialized,
    login,
    register,
    logout,
    checkAuth
  }
})
