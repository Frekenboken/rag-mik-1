<template>
  <div class="chat-container">
    <!-- История сообщений -->
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" :class="['message', `message-${message.role}`]">
        <div class="message-header">
          <span class="message-role">
            {{ message.role === 'user' ? 'Вы' : 'Ассистент' }}
          </span>
          <span class="message-time">
            {{ formatTime(message.timestamp) }}
          </span>
        </div>

        <div class="message-content">
          {{ message.content }}
        </div>

        <!-- Метаданные ответа -->
        <div v-if="message.role === 'assistant' && message.sources" class="message-meta">
          <div v-if="message.sources.length" class="sources">
            <strong>Источники:</strong>
            <span v-for="(source, index) in message.sources" :key="index">
              {{ source }}{{ index < message.sources.length - 1 ? ', ' : '' }} </span>
          </div>

          <div v-if="message.confidence" class="confidence">
            <strong>Уверенность:</strong>
            {{ (message.confidence * 100).toFixed(1) }}%
          </div>

          <div v-if="message.relatedTopics?.length" class="topics">
            <strong>Связанные темы:</strong>
            <span v-for="(topic, index) in message.relatedTopics" :key="index">
              {{ topic }}{{ index < message.relatedTopics.length - 1 ? ', ' : '' }} </span>
          </div>
        </div>
      </div>

      <!-- Индикатор загрузки -->
      <div v-if="isLoading" class="loading-indicator">
        <div class="typing-animation">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <!-- Форма ввода -->
    <form @submit.prevent="handleSubmit" class="chat-input-form">
      <div class="input-group">
        <input v-model="userInput" type="text" placeholder="Задайте ваш вопрос..." :disabled="isLoading"
          class="chat-input" @keydown.enter.prevent="handleSubmit" />

        <button type="submit" :disabled="!userInput.trim() || isLoading" class="send-button">
          <span v-if="!isLoading">Отправить</span>
          <span v-else>Отправка...</span>
        </button>
      </div>

      <button v-if="messages.length > 0" type="button" @click="clearChat" class="clear-button">
        Очистить историю
      </button>
    </form>

    <!-- Сообщение об ошибке -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue';
import { useChatStore } from '../stores/chat';

const userInput = ref('');
const messagesContainer = ref(null);

const chatStore = useChatStore();
const { messages, isLoading, error, sendQuestion, clearChat } = chatStore;

// Автопрокрутка к последнему сообщению
watch(messages, async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
});

const handleSubmit = async () => {
  if (!userInput.value.trim() || isLoading) return;

  const question = userInput.value.trim();
  userInput.value = '';

  try {
    await sendQuestion(question);
  } catch (err) {
    console.error('Error in handleSubmit:', err);
  }
};

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  background: #fafafa;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 80%;
  word-wrap: break-word;
}

.message-user {
  align-self: flex-end;
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-assistant {
  align-self: flex-start;
  background-color: white;
  color: #333;
  border: 1px solid #e0e0e0;
  border-bottom-left-radius: 4px;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 12px;
  opacity: 0.8;
}

.message-content {
  line-height: 1.5;
}

.message-meta {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px dashed #e0e0e0;
  font-size: 12px;
  color: #666;
}

.message-meta>div {
  margin-top: 4px;
}

.loading-indicator {
  align-self: flex-start;
  padding: 12px 16px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  border-bottom-left-radius: 4px;
}

.typing-animation {
  display: flex;
  align-items: center;
  height: 20px;
}

.typing-animation span {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: #999;
  border-radius: 50%;
  margin: 0 2px;
  animation: typing 1.4s infinite;
}

.typing-animation span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-animation span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {

  0%,
  100% {
    transform: translateY(0);
    opacity: 0.4;
  }

  50% {
    transform: translateY(-5px);
    opacity: 1;
  }
}

.chat-input-form {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: white;
}

.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 24px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input:focus {
  border-color: #007bff;
}

.chat-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.send-button {
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.send-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.clear-button {
  width: 100%;
  padding: 8px 16px;
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.clear-button:hover {
  background-color: #e9ecef;
}

.error-message {
  padding: 12px 20px;
  background-color: #f8d7da;
  color: #721c24;
  border-top: 1px solid #f5c6cb;
  font-size: 14px;
}
</style>