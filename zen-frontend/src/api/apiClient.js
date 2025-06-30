import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getQuiz = (userMessage) => {
  return apiClient.get('/quiz/', { params: { user_message: userMessage } });
};

export const startMeditation = (payload) => {
  return apiClient.post('/meditate', payload);
};

export const submitFeedback = (payload) => {
  return apiClient.post('/feedback', payload);
};

export default apiClient;
