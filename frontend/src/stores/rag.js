import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { API } from '../api/rag';

export const useRagStore = defineStore('rag', () => {
  // State
  const messages = ref([]);
  const isLoading = ref(false);
  const documentsLoading = ref(false);
  const error = ref(null);
  const documents = ref([]);

  // Getters
  const context = computed(() => {
    return messages.value.slice(-6)
      .map(msg => `${msg.role}: ${msg.content}`)
      .join('\n');
  });

  const documentsCount = computed(() => documents.value.length);

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
      const response = await API.postQuery(req);

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

  // Документы
  const fetchDocuments = async () => {
    documentsLoading.value = true;
    error.value = null;

    try {
      const response = await API.getDocs();
      
      if (response.data && Array.isArray(response.data.documents)) {
        documents.value = response.data.documents;
      } else if (Array.isArray(response.data)) {
        documents.value = response.data;
      } else {
        documents.value = [];
      }
      
      return response;
    } catch (err) {
      error.value = err.message || 'Ошибка при загрузке документов';
      documents.value = [];
      throw err;
    } finally {
      documentsLoading.value = false;
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
    documentsLoading,
    error,
    documents,
    
    // Getters
    context,
    documentsCount,
    
    // Actions
    sendQuestion,
    addMessage,
    clearChat,
    fetchDocuments
  };
});