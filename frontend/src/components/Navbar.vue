<template>
  <nav class="bg-primary/10 rounded-xl p-1">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex justify-between h-16 items-center">
        <!-- Логотип -->
        <div class="flex-shrink-0 flex items-center">
          <router-link to="/">
            <div>
              <h1 class="text-md 2xl:text-2xl font-bold text-primary">
                RAG System
              </h1>
              <p class="text-xs hidden 2xl:block text-base-content opacity-70">
                Помощь в эксплуатации МИК-1
              </p>
            </div>
          </router-link>
        </div>

        <!-- Десктопное меню -->
        <div class="hidden md:flex space-x-4 items-center">
          <router-link v-for="item in menuItems" :key="item.name" :to="item.to" class="btn btn-ghost rounded-btn">
            {{ item.name }}
          </router-link>

          <!-- Аватар + меню -->
          <div v-if="isAuthenticated" class="dropdown dropdown-end">
            <label tabindex="0" class="btn btn-ghost btn-circle avatar">
              <div class="w-10 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                <img :src="`https://ui-avatars.com/api/?name=${user.email}&size=256&background=222&color=999`"
                  alt="avatar" />
              </div>
            </label>
            <ul tabindex="0" class="menu menu-md dropdown-content bg-base-300 rounded-b-xl shadow-md mt-4 w-30">
              <!-- <li><router-link to="/profile">👤 Профиль</router-link></li>
              <li><router-link to="/settings">⚙ Настройки</router-link></li> -->
              <li><button @click="onLogout">🚪 Выйти</button></li>
            </ul>
          </div>
        </div>

        <!-- Бургер -->
        <div class="flex items-center md:hidden">
          <button @click="isOpen = !isOpen" class="btn btn-ghost">
            <svg v-if="!isOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Мобильное меню -->
    <div v-if="isOpen" class="md:hidden px-2 pt-2 pb-3 space-y-1 bg-base-100 shadow">
      <router-link v-for="item in menuItems" :key="item.name + '-mobile'" :to="item.to"
        class="btn btn-ghost w-full justify-start">
        {{ item.name }}
      </router-link>
      <button v-if="isAuthenticated" @click="onLogout" class="btn btn-error w-full justify-start">
        🚪 Выйти
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

const auth = useAuthStore()
const { user, isAuthenticated } = storeToRefs(auth)
const router = useRouter()
const isOpen = ref(false)

const onLogout = async () => {
  const success = await auth.logout()
  if (success) router.push('/login')
  else alert('Не удалось выйти. Попробуйте ещё раз.')
}

const menuItems = computed(() => {
  if (!isAuthenticated.value) {
    return [
      { name: 'Вход', to: '/login' },
      { name: 'Регистрация', to: '/register' }
    ]
  }
})
</script>
