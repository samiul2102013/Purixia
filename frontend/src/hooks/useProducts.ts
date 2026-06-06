import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { catalogService } from '../services/catalog';

export function useProducts(params?: {
  category?: string;
  in_stock?: boolean;
  page?: number;
}) {
  return useQuery({
    queryKey: ['products', params],
    queryFn: () => catalogService.getProducts(params),
    staleTime: 2 * 60 * 1000, // 2 minutes
    placeholderData: keepPreviousData,
  });
}

export function useProduct(id: number | string) {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => catalogService.getProduct(id),
    enabled: !!id,
  });
}
