<template>
  <div class="flex-grow flex flex-col p-2">
    <div class="grid grid-cols-1 md:grid-cols-6 gap-2 flex-grow">
      <div class="col-span-6 max-h-full flex items-center justify-center">
        <div class="bg-base-100 p-10 rounded-xl shadow-lg w-full max-w-md">
          <h1 class="text-2xl font-bold mb-6 text-center text-primary">Регистрация</h1>
          <form @submit.prevent="onSubmit" class="space-y-4">
            <div>
              <label class="block text-base-content mb-1">Email</label>
              <input v-model="email" type="email" required
                class="bg-base-200 text-base-content w-full px-4 py-2 border border-base-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none" />
            </div>
            <div>
              <label class="block text-base-content mb-1">Пароль</label>
              <input v-model="password" type="password" required
                class="bg-base-200 text-base-content w-full px-4 py-2 border border-base-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none" />
            </div>
            <button :disabled="loading"
              class="w-full bg-primary text-primary-content py-2 rounded-lg hover:bg-primary/90 transition disabled:opacity-50">
              {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>
          </form>
          <p class="mt-4 text-base-content text-center">
            Уже есть аккаунт?
            <router-link to="/login" class="text-secondary hover:underline">Войти</router-link>
          </p>
          <p v-if="error" class="mt-3 text-error text-center">{{ error }}</p>
        </div>
      </div>
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
