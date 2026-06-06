import { create } from 'zustand';
import { User } from '../types';
import { authService, saveTokens, clearTokens, getAccessToken, getRefreshToken } from '../services/auth';
import { useCartStore } from './cartStore';

interface AuthState {
  user: User | null;
  isLoggedIn: boolean;
  loading: boolean;
  setUser: (user: User | null) => void;
  clearUser: () => void;
  initAuth: () => Promise<void>;
  login: (username: string, password: string) => Promise<User>;
  register: (data: any) => Promise<User>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isLoggedIn: false,
  loading: true,

  setUser: (user) => set({ user, isLoggedIn: !!user }),
  
  clearUser: () => set({ user: null, isLoggedIn: false }),

  initAuth: async () => {
    set({ loading: true });
    const token = getAccessToken();
    if (token) {
      try {
        const user = await authService.me();
        set({ user, isLoggedIn: true });
      } catch (error) {
        // Token might be expired or invalid, clear it
        clearTokens();
        set({ user: null, isLoggedIn: false });
      }
    }
    set({ loading: false });
  },

  login: async (username, password) => {
    set({ loading: true });
    try {
      const response = await authService.login({ username, password });
      saveTokens(response.tokens);
      set({ user: response.user, isLoggedIn: true, loading: false });
      
      // Sync cart after login
      await useCartStore.getState().fetchCart();
      
      return response.user;
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },

  register: async (data) => {
    set({ loading: true });
    try {
      const response = await authService.register(data);
      saveTokens(response.tokens);
      set({ user: response.user, isLoggedIn: true, loading: false });
      
      // Sync cart after registration
      await useCartStore.getState().fetchCart();
      
      return response.user;
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },

  logout: async () => {
    set({ loading: true });
    const refresh = getRefreshToken();
    if (refresh) {
      try {
        await authService.logout(refresh);
      } catch (error) {
        console.error('Failed to blacklist token on backend logout', error);
      }
    }
    clearTokens();
    set({ user: null, isLoggedIn: false, loading: false });
    
    // Sync cart after logout (should clear it or show anonymous cart)
    await useCartStore.getState().fetchCart();
  },
}));
