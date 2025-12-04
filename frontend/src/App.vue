<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div data-theme="">



    <!-- Верхний блок (на всю высоту экрана) -->
    <div class="min-h-screen flex flex-col bg-base-300">
      <!-- Навбар -->
      <Navbar></Navbar>

      <router-view />

    </div>

    <!-- Нижний блок (ниже экрана) -->
    <div class="min-h-screen bg-gray-800 text-white p-4">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-2xl font-bold mb-4">Нижний блок (ниже экрана)</h2>
        <div class="bg-gray-700 border border-gray-600 rounded-lg shadow p-6">
          <p class="text-gray-300">Этот блок начинается после того, как закончился верхний блок. Он находится ниже
            экрана при первоначальной загрузке страницы.</p>
        </div>

        <!-- Футер -->
        <footer class="mt-8 pt-8 border-t border-gray-700">
          <div class="flex flex-col md:flex-row justify-between items-center">
            <div class="mb-4 md:mb-0">
              <p class="text-gray-400">© 2023 Мой проект. Все права защищены.</p>
            </div>
            <div>
              <ul class="flex space-x-6">
                <li><a class="text-gray-400 hover:text-white">Политика конфиденциальности</a></li>
                <li><a class="text-gray-400 hover:text-white">Условия использования</a></li>
                <li><a class="text-gray-400 hover:text-white">Контакты</a></li>
              </ul>
            </div>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>
