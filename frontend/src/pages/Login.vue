<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-10 rounded-xl shadow-lg w-full max-w-md">
      <h1 class="text-2xl font-bold mb-6 text-center text-blue-600">Вход</h1>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-gray-700 mb-1">Email</label>
          <input v-model="email" type="email" required
            class="text-accent-content w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" />
        </div>

        <div>
          <label class="block text-gray-700 mb-1">Пароль</label>
          <input v-model="password" type="password" required
            class="text-accent-content w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" />
        </div>

        <button :disabled="loading" class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <p class="mt-4 text-gray-600 text-center">
        Нет аккаунта? <router-link to="/register" class="text-green-600 hover:underline">Регистрация</router-link>
      </p>

      <p v-if="error" class="mt-3 text-red-500 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const onSubmit = async () => {
  loading.value = true
  error.value = null
  try {
    await auth.login({ email: email.value, password: password.value })
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}
</script>
