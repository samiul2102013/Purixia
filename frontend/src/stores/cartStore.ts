import { create } from 'zustand';
import { CartItem, CartResponse } from '../types';
import { cartService } from '../services/cart';

interface CartState {
  items: CartItem[];
  count: number;
  grandTotal: string;
  loading: boolean;
  isDrawerOpen: boolean;
  
  setCart: (cart: CartResponse) => void;
  openDrawer: () => void;
  closeDrawer: () => void;
  toggleDrawer: () => void;
  fetchCart: () => Promise<void>;
  addItem: (productId: number | string, quantity?: number) => Promise<void>;
  updateItem: (productId: number | string, quantity: number) => Promise<void>;
  removeItem: (productId: number | string) => Promise<void>;
  clearCart: () => Promise<void>;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  count: 0,
  grandTotal: '0.00',
  loading: false,
  isDrawerOpen: false,

  setCart: (cart) => set({
    items: cart.items || [],
    grandTotal: cart.grand_total || '0.00',
    count: cart.count || 0,
  }),

  openDrawer: () => set({ isDrawerOpen: true }),
  
  closeDrawer: () => set({ isDrawerOpen: false }),
  
  toggleDrawer: () => set((state) => ({ isDrawerOpen: !state.isDrawerOpen })),

  fetchCart: async () => {
    set({ loading: true });
    try {
      const cart = await cartService.getCart();
      get().setCart(cart);
    } catch (error: any) {
      console.error('Failed to fetch cart', error);
      // If unauthorized, we might need to handle it or clear state
      if (error.response?.status === 401) {
        set({ items: [], count: 0, grandTotal: '0.00' });
      }
    } finally {
      set({ loading: false });
    }
  },

  addItem: async (productId, quantity = 1) => {
    set({ loading: true });
    try {
      await cartService.addItem(productId, quantity);
      await get().fetchCart();
      get().openDrawer(); // Open drawer when item added as per nice premium feel
    } catch (error) {
      console.error('Failed to add item to cart', error);
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  updateItem: async (productId, quantity) => {
    set({ loading: true });
    try {
      await cartService.updateItem(productId, quantity);
      await get().fetchCart();
    } catch (error) {
      console.error('Failed to update cart item', error);
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  removeItem: async (productId) => {
    set({ loading: true });
    try {
      await cartService.removeItem(productId);
      await get().fetchCart();
    } catch (error) {
      console.error('Failed to remove cart item', error);
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  clearCart: async () => {
    set({ loading: true });
    try {
      await cartService.clearCart();
      set({
        items: [],
        grandTotal: '0.00',
        count: 0,
      });
    } catch (error) {
      console.error('Failed to clear cart', error);
      throw error;
    } finally {
      set({ loading: false });
    }
  },
}));
