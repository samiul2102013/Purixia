import api from '../lib/axios';
import { User, Tokens, AuthResponse } from '../types';

export const saveTokens = (tokens: Tokens): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  }
};

export const clearTokens = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};

export const getAccessToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
};

export const getRefreshToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('refresh_token');
  }
  return null;
};

export const isAuthenticated = (): boolean => {
  return !!getAccessToken();
};

export const authService = {
  register: async (data: any): Promise<AuthResponse> => {
    const response = await api.post('/api/auth/register/', data);
    return response.data;
  },

  login: async (data: any): Promise<AuthResponse> => {
    const response = await api.post('/api/auth/login/', data);
    return response.data;
  },

  logout: async (refresh: string): Promise<void> => {
    await api.post('/api/auth/logout/', { refresh });
  },

  refreshToken: async (refresh: string): Promise<{ access: string }> => {
    const response = await api.post('/api/auth/token/refresh/', { refresh });
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await api.get('/api/auth/me/');
    return response.data;
  },

  updateMe: async (data: Partial<User>): Promise<User> => {
    const response = await api.patch('/api/auth/me/', data);
    return response.data;
  },
};
