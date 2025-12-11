<template>
  <main class="flex-grow flex flex-col p-2">
    <div class="grid grid-cols-1 md:grid-cols-6 gap-2 flex-grow">
      <!-- Chat занимает 4 колонки -->
      <div class="md:col-span-5 relative overflow-auto">
        <Chat class="absolute inset-0 overflow-auto"></Chat>
      </div>

      <!-- Documents занимает 2 колонки -->
      <div class="md:col-span-1 relative overflow-auto">
        <Documents class="absolute inset-0 overflow-auto"></Documents>
      </div>
    </div>
  </main>
</template>

<script setup>
import Chat from '../components/Chat.vue';
import Documents from '../components/Documents.vue';


</script>