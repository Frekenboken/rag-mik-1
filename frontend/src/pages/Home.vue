<template>
  <main class="flex-grow flex flex-col p-2">
    <div class="grid grid-cols-1 md:grid-cols-6 gap-2 flex-grow">
      <!-- Documents теперь занимает 1 колонку с вложенной структурой -->
      <div class="md:col-span-1 relative overflow-auto">
        <div class="absolute inset-0 flex flex-col gap-2">
          <!-- Навбар -->
          <Navbar></Navbar>
          <!-- Documents с прокруткой -->
          <div class="flex-grow overflow-auto">
            <Documents class="h-full"></Documents>
          </div>
        </div>
      </div>

      <div class="md:col-span-1 relative overflow-auto">
      </div>

      <!-- Chat занимает 4 колонки -->
      <div class="md:col-span-3 relative overflow-auto">
        <Chat class="absolute inset-0 overflow-auto"></Chat>
      </div>
    </div>
  </main>
</template>

<script setup>
import Chat from '../components/Chat.vue';
import Documents from '../components/Documents.vue';
import Navbar from '../components/Navbar.vue';


</script>