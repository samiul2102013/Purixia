import api from '../lib/axios';
import { Banner } from '../types';

export const bannerService = {
  getBanners: async (): Promise<Banner[]> => {
    const response = await api.get('/api/banners/');
    if (Array.isArray(response.data)) {
      return response.data;
    }
    if (response.data && Array.isArray(response.data.results)) {
      return response.data.results;
    }
    return [];
  },
};
