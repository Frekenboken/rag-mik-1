<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div data-theme="forest">



    <!-- Верхний блок (на всю высоту экрана) -->
    <div class="min-h-screen flex flex-col bg-base-300">
      <!-- Навбар -->
      <Navbar></Navbar>

      <router-view />

    </div>

    <!-- Нижний блок (ниже экрана) -->
    <div class="bg-base-100 text-base-content p-4">
      <div class="max-w-7xl mx-auto">

        <!-- Футер -->
        <footer class="mt-12 pt-8 border-t border-gray-700">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
            <!-- О проекте -->
            <div>
              <h3 class="text-lg font-semibold text-base-content mb-3">РАГ-система обслуживания МИК-1</h3>
              <p class="text-sm text-base-content/70">
                Интеллектуальная система на основе Retrieval-Augmented Generation для помощи специалистам в диагностике,
                ремонте и техническом обслуживании комплекса МИК-1.
              </p>
              <p class="text-xs text-base-content/50 mt-4">Версия 1.0.0 • 2025</p>
            </div>

            <!-- Создатели и контакты -->
            <div>
              <h3 class="text-lg font-semibold text-base-content mb-3">Разработчики</h3>
              <ul class="text-sm text-base-content/70 space-y-2">
                <li>Ведущий разработчик: Иванов И.И.</li>
                <li>ML-инженер: Петрова А.С.</li>
                <li>Backend: Сидоров Д.В.</li>
                <li>Frontend: Козлова Е.Н.</li>
              </ul>
              <div class="mt-4">
                <p class="text-sm text-base-content/70">
                  Контакты: <a href="mailto:support@mik1-rag.ru"
                    class="link link-accent hover:link-hover">support@mik1-rag.ru</a>
                </p>
                <p class="text-sm text-base-content/70">
                  Тел.: <a href="tel:+78005553535" class="link link-accent hover:link-hover">+7 (800) 555-35-35</a>
                </p>
              </div>
            </div>

            <!-- Ссылки -->
            <div>
              <h3 class="text-lg font-semibold text-base-content mb-3">Полезные ссылки</h3>
              <ul class="text-sm space-y-2">
                <li><a href="#" class="link link-accent hover:link-hover">Документация</a></li>
                <li><a href="#" class="link link-accent hover:link-hover">Руководство пользователя</a></li>
                <li><a href="#" class="link link-accent hover:link-hover">Политика конфиденциальности</a></li>
                <li><a href="#" class="link link-accent hover:link-hover">Условия использования</a></li>
                <li><a href="#" class="link link-accent hover:link-hover">Обратная связь</a></li>
              </ul>
            </div>
          </div>

          <!-- Нижняя строка с копирайтом -->
          <div class="mt-10 pt-6 border-t border-gray-700 text-center">
            <p class="text-sm text-base-content/60">
              © 2025 РАГ-система обслуживания МИК-1. Все права защищены.
            </p>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>
