<template>
  <nav class="bg-base-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Логотип -->
        <div class="flex-shrink-0 flex items-center">
          <router-link to="/">
            <div>
              <h1 class="text-2xl lg:text-2xl font-bold text-primary">
                CargoFlow
                <template v-if="user?.role === 'admin'">Admin</template>
                <template v-else-if="user?.role === 'manager'">Manager</template>
                <template v-else-if="user?.role === 'driver'">Driver</template>
                <template v-else>User</template>
              </h1>
              <p class="text-xs text-base-content opacity-70">
                <template v-if="user?.role === 'admin'">
                  🔧 Панель администратора
                </template>
                <template v-else-if="user?.role === 'manager'">
                  📊 Панель управления перевозками
                </template>
                <template v-else-if="user?.role === 'driver'">
                  🚛 Мобильный рабочий кабинет
                </template>
                <template v-else>
                  Система управления грузоперевозками
                </template>
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
                <img :src="user.value?.avatar || 'https://i.pravatar.cc/100?u=f' + user.value?.email" alt="avatar" />
              </div>
            </label>
            <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box shadow-md mt-3 w-52">
              <li><router-link to="/profile">👤 Профиль</router-link></li>
              <li><router-link to="/settings">⚙ Настройки</router-link></li>
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
      { name: 'Главная', to: '/' },
      { name: 'Вход', to: '/login' },
      { name: 'Регистрация', to: '/register' }
    ]
  }
})
</script>
