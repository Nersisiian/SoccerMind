import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
});

api.interceptors.request.use(async (config) => {
  // Получаем токен из next-auth сессии или localStorage
  if (typeof window !== 'undefined') {
    const session = await import('next-auth/react').then((m) => m.getSession());
    if (session?.accessToken) {
      config.headers.Authorization = `Bearer ${session.accessToken}`;
    }
  }
  return config;
});

export default api;
export const fetcher = (url: string) => api.get(url).then(res => res.data);
