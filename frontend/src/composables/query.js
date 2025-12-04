// hooks/usePost.js
import { ref } from 'vue';
import axios from 'axios';

export function usePost(url) {
  const data = ref(null);
  const error = ref(null);
  const loading = ref(false);

  const post = async (body, config = {}) => {
    loading.value = true;
    error.value = null;
    data.value = null;

    try {
      const response = await axios.post(url, body, config);
      data.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    data,
    error,
    loading,
    post
  };
}