<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-10 rounded-xl shadow-lg w-full max-w-md">
      <h1 class="text-2xl font-bold mb-6 text-center text-green-600">Регистрация</h1>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-gray-700 mb-1">Email</label>
          <input v-model="email" type="email" required
            class="text-accent-content w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none" />
        </div>

        <div>
          <label class="block text-gray-700 mb-1">Пароль</label>
          <input v-model="password" type="password" required
            class="text-accent-content w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none" />
        </div>

        <button :disabled="loading"
          class="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="mt-4 text-gray-600 text-center">
        Уже есть аккаунт? <router-link to="/login" class="text-blue-600 hover:underline">Войти</router-link>
      </p>

      <p v-if="error" class="mt-3 text-red-500 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const firstname = ref('')
const lastname = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const router = useRouter()
const auth = useAuthStore()

const onSubmit = async () => {
  loading.value = true
  error.value = null
  try {
    await auth.register({
      firstname: firstname.value,
      lastname: lastname.value,
      email: email.value,
      password: password.value
    })
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>
