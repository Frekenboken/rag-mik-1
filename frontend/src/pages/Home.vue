<template>

  <!-- Основное содержимое верхнего блока -->
  <main class="flex-grow flex flex-col p-2">
    <!-- 3 блока под навбаром -->
    <div class="grid grid-cols-1 md:grid-cols-6 gap-2 flex-grow">
      <!-- Блок 1 -->
      <!-- <div class="bg-white border border-gray-300 rounded-lg shadow p-4">
        <h2 class="text-lg font-bold mb-2">Блок 1</h2>
        <p class="text-gray-600">Содержимое блока 1</p>
      </div> -->

      <!-- Блок 2 -->
      <!-- <div class="bg-white border border-gray-300 rounded-lg shadow p-4">
        <h2 class="text-lg font-bold mb-2">Блок 2</h2>
        <p class="text-gray-600">Содержимое блока 2</p>
      </div> -->

      <!-- Блок 3 -->
      <!-- <div class="bg-white border border-gray-300 rounded-lg shadow p-4">
        <h2 class="text-lg font-bold mb-2">Блок 3</h2>
        <p class="text-gray-600">Содержимое блока 3</p>
      </div> -->


      <Documents></Documents>

      <Chat class="col-span-4 max-h-full"></Chat>

      <Documents></Documents>


    </div>

    <!-- Индикатор, что это конец верхнего блока -->
    <div class="text-center py-4 mt-4 border-t border-gray-300">
      <p class="text-gray-500">Верхний блок (занимает всю высоту экрана)</p>
    </div>
  </main>
  <!-- <div class="min-h-screen flex flex-col items-center">
    <Chat></Chat>
  </div> -->
</template>

<script setup>
import Chat from '../components/Chat.vue';
import Documents from '../components/Documents.vue';


</script>