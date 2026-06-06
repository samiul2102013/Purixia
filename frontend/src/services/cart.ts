import api from '../lib/axios';
import { CartResponse } from '../types';

export const cartService = {
  getCart: async (): Promise<CartResponse> => {
    const response = await api.get('/api/cart/');
    return response.data;
  },

  addItem: async (productId: number | string, quantity = 1): Promise<any> => {
    const response = await api.post('/api/cart/', {
      product_id: productId,
      quantity,
    });
    return response.data;
  },

  updateItem: async (productId: number | string, quantity: number): Promise<any> => {
    const response = await api.patch('/api/cart/', {
      product_id: productId,
      quantity,
    });
    return response.data;
  },

  removeItem: async (productId: number | string): Promise<any> => {
    const response = await api.delete('/api/cart/', {
      data: { product_id: productId },
    });
    return response.data;
  },

  clearCart: async (): Promise<any> => {
    const response = await api.delete('/api/cart/clear/');
    return response.data;
  },
};
