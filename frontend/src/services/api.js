import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor — attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('castpod_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor — handle 401 (expired/invalid token)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('castpod_token');
      localStorage.removeItem('castpod_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ─── Auth API ─────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
};

// ─── Sessions API ─────────────────────────────────────
export const sessionsAPI = {
  list: () => api.get('/api/sessions'),
  get: (id) => api.get(`/api/sessions/${id}`),
};

// ─── Upload API ───────────────────────────────────────
export const uploadAPI = {
  uploadPdf: (file, mode) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', mode);
    return api.post('/api/upload-pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 300000, // 5 min timeout for processing
    });
  },
};

// ─── Questions API ────────────────────────────────────
export const questionsAPI = {
  ask: (sessionId, question) =>
    api.post('/api/ask-question', { session_id: sessionId, question }),
};

export default api;
