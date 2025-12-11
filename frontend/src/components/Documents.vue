<template>
    <!-- Sidebar -->
    <aside class="border-r border-base-300 p-4 flex flex-col gap-4 bg-base-100 rounded-xl">
        <div class="text-xl font-semibold mb-2">База знаний</div>

        <!-- File List -->
        <div class="flex-1 overflow-y-auto space-y-2 pr-1 custom-scroll">
            <div v-for="doc in documents" :key="doc.id"
                class="p-3 rounded-xl border border-base-300 hover:bg-base-200 transition cursor-pointer select-none">
                <div class="font-medium truncate">{{ doc.name }}</div>
                <div class="text-xs opacity-60">{{ doc.size }} MB • {{ doc.extension }}</div>
            </div>
        </div>

        <!-- Upload button -->
        <button class="btn btn-disabled rounded-xl" tabindex="-1" role="button" aria-disabled="true">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            Загрузить файлы
        </button>
    </aside>

</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRagStore } from '../stores/rag';
import { storeToRefs } from 'pinia'

const ragStore = useRagStore();
const { documents } = storeToRefs(ragStore)

onMounted(() => {
    // Загружаем документы при загрузке компонента
    ragStore.fetchDocuments();
});


// // Data
// const files = ref([
//     { id: 1, name: 'documentation.pdf', size: 4.1, type: 'PDF', uploaded: '2024-01-15' },
//     { id: 2, name: 'architecture.md', size: 0.8, type: 'Markdown', uploaded: '2024-01-14' },
//     { id: 3, name: 'requirements.txt', size: 0.2, type: 'Text', uploaded: '2024-01-13' }
// ])


</script>