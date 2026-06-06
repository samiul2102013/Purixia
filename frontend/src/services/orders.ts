import api from '../lib/axios';
import { Order, PlaceOrderPayload, PaginatedResponse } from '../types';

export const orderService = {
  placeOrder: async (payload: PlaceOrderPayload): Promise<Order> => {
    const response = await api.post('/api/orders/place/', payload);
    return response.data;
  },

  getMyOrders: async (): Promise<PaginatedResponse<Order>> => {
    const response = await api.get('/api/orders/');
    return response.data;
  },

  getOrder: async (id: number | string): Promise<Order> => {
    const response = await api.get(`/api/orders/${id}/`);
    return response.data;
  },
};
