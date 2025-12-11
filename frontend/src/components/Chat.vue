<template>
    <div class="flex bg-base-200 text-base-content">

        <!-- Chat Area -->
        <main class="flex-1 flex flex-col">
            <!-- Header -->
            <div class="border-b border-base-300 p-4 flex items-center justify-between bg-base-100">
                <div class="flex items-center gap-3">
                    <div class="text-lg font-semibold">Чат</div>
                    <div class="badge badge-primary">v1.0</div>
                </div>
                <div class="flex items-center gap-3">
                    <button class="btn btn-sm rounded-xl btn-outline" @click="clearChat"
                        :disabled="messages.length === 0">
                        Очистить чат
                    </button>
                </div>
            </div>

            <!-- Messages Container -->
            <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-6 custom-scroll">
                <div v-for="message in messages" :key="message.id"
                    :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start']">
                    <div class="flex flex-col max-w-xl">
                        <!-- Бабл сообщения -->
                        <div :class="[
                            'px-4 py-3 rounded-2xl shadow border text-sm',
                            message.role === 'user'
                                ? 'bg-primary text-primary-content border-primary/20 rounded-br-none'
                                : 'bg-base-100 border-base-300 rounded-bl-none'
                        ]">
                            <!-- Заголовок: Вы / Помощник -->
                            <div class="font-semibold text-xs mb-2 opacity-70">
                                {{ message.role === 'user' ? 'Вы' : 'Помощник' }}
                            </div>

                            <!-- Контент с Markdown -->
                            <div class="message-content" v-html="parseMarkdown(message.content)">
                            </div>
                        </div>

                        <!-- Время -->
                        <div :class="[
                            'text-xs mt-1 px-2',
                            message.role === 'user' ? 'text-right text-primary/60' : 'text-base-content/60'
                        ]">
                            {{ formatTime(message.timestamp) }}
                        </div>
                    </div>
                </div>

                <!-- Loading indicator -->
                <div v-if="isLoading" class="flex justify-start">
                    <div class="max-w-xl p-4 rounded-2xl bg-base-100 border border-base-300">
                        <div class="flex items-center gap-2">
                            <div class="loading loading-dots loading-sm"></div>
                            <span class="text-sm">Думаю... {{ elapsedTime }} сек.</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input Area -->
            <div class="p-4 border-t border-base-300 bg-base-100">
                <form @submit.prevent="handleSubmit">
                    <div class="flex gap-3 items-end">
                        <div class="flex-1 relative">
                            <textarea v-model="userInput" ref="textareaRef" rows="1"
                                class="textarea textarea-bordered w-full rounded-2xl resize-none min-h-[48px] max-h-32 py-3 pr-12"
                                :disabled="isLoading" placeholder="Задайте свой вопрос..."
                                @keydown.enter.exact.prevent="handleSubmit" @input="autoResize" />
                            <div class="absolute right-3 bottom-3 text-xs opacity-50">
                                ↵ Enter
                            </div>
                        </div>
                        <button type="submit" :disabled="!userInput.trim() || isLoading"
                            class="btn btn-primary px-6 rounded-xl h-[48px] min-w-[100px]"
                            :class="{ 'opacity-50 cursor-not-allowed': !userInput.trim() || isLoading }">
                            <span v-if="!isLoading">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                </svg>
                            </span>
                            <span v-else class="loading loading-spinner"></span>
                        </button>
                    </div>
                </form>

                <!-- Error message -->
                <div v-if="error" class="mt-3">
                    <div class="alert alert-error rounded-xl">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>{{ error }}</span>
                        <button class="btn btn-sm btn-ghost" @click="error = ''">Dismiss</button>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRagStore } from '../stores/rag'
import { storeToRefs } from 'pinia'

import { marked } from 'marked';


// Refs
const userInput = ref('')
const textareaRef = ref(null)
const messagesContainer = ref(null)
const selectedFile = ref(null)

// Store
const chatStore = useRagStore()
const { sendQuestion, clearChat } = chatStore
const { messages, isLoading, error } = storeToRefs(chatStore)

const elapsedTime = ref(0)
let timer = null

watch(isLoading, (newVal) => {
    if (newVal) {
        // Начало загрузки
        elapsedTime.value = 0
        timer = setInterval(() => {
            elapsedTime.value++
        }, 1000)
    } else {
        // Конец загрузки
        if (timer) {
            clearInterval(timer)
            timer = null
        }
    }
})

// Methods
const autoResize = () => {
    if (textareaRef.value) {
        textareaRef.value.style.height = 'auto'
        textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 128) + 'px'
    }
}

const handleSubmit = async () => {
    if (!userInput.value.trim() || isLoading.value) return

    const question = userInput.value.trim()
    userInput.value = ''
    autoResize() // Reset textarea height

    try {
        await sendQuestion(question)
    } catch (err) {
        console.error('Error in handleSubmit:', err)
    }
}

const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const parseMarkdown = (text) => {
    return marked(text || '');
};

// Watchers
watch(messages, async () => {
    await nextTick()
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
})

watch(userInput, () => {
    nextTick(autoResize)
})

// Lifecycle
onMounted(() => {
    // Фокус на поле ввода при загрузке
    textareaRef.value?.focus()
})

onUnmounted(() => {
    if (timer) clearInterval(timer)
})
</script>

<style scoped>
.custom-scroll {
    scrollbar-width: thin;
    scrollbar-color: hsl(var(--bc) / 0.2) transparent;
}

.custom-scroll::-webkit-scrollbar {
    width: 6px;
}

.custom-scroll::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scroll::-webkit-scrollbar-thumb {
    background-color: hsl(var(--bc) / 0.2);
    border-radius: 3px;
}

.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.message-transition {
    transition: all 0.3s ease;
}
</style>