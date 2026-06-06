import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { orderService } from '../services/orders';
import { useAuthStore } from '../stores/authStore';
import toast from 'react-hot-toast';

export function useOrders() {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);

  return useQuery({
    queryKey: ['orders'],
    queryFn: orderService.getMyOrders,
    enabled: isLoggedIn,
  });
}

export function useOrder(id: number | string) {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);

  return useQuery({
    queryKey: ['order', id],
    queryFn: () => orderService.getOrder(id),
    enabled: isLoggedIn && !!id,
  });
}

export function usePlaceOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: orderService.placeOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to place order. Try again.';
      toast.error(message);
    },
  });
}
