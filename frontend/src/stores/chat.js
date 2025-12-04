import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { API } from '../api/query';

export const useChatStore = defineStore('chat', () => {
  // State
  const messages = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  // Getters
  const context = computed(() => {
    // Формируем контекст из последних N сообщений
    return messages.value
      .map(msg => `${msg.role}: ${msg.content}`)
      .join('\n');
  });

  // Actions
  const addMessage = (role, content, metadata = {}) => {
    messages.value.push({
      id: Date.now(),
      role, // 'user' или 'assistant'
      content,
      timestamp: new Date().toISOString(),
      ...metadata
    });
  };

  const sendQuestion = async (question) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Добавляем вопрос пользователя
      addMessage('user', question);

      const req = {
        question: question,
        context: context.value
      };

      console.log(messages);

      // Отправляем на сервер с контекстом
      const response = await API.getQuery(req);

      // Добавляем ответ ассистента
      addMessage('assistant', response.data.answer, {
        sources: response.data.sources,
        confidence: response.data.confidence,
        relatedTopics: response.data.related_topics
      });

      return response;
    } catch (err) {
      error.value = err.message || 'Произошла ошибка при отправке вопроса';
      
      // Добавляем сообщение об ошибке
      addMessage('assistant', 'Извините, произошла ошибка. Пожалуйста, попробуйте позже.');
      
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const clearChat = () => {
    messages.value = [];
    error.value = null;
  };

  return {
    // State
    messages,
    isLoading,
    error,
    
    // Getters
    context,
    
    // Actions
    sendQuestion,
    addMessage,
    clearChat
  };
});