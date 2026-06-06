import { useQuery } from '@tanstack/react-query';
import { catalogService } from '../services/catalog';

export function useCategories() {
  return useQuery({
    queryKey: ['categories'],
    queryFn: catalogService.getCategories,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCategoryDetail(slug: string) {
  return useQuery({
    queryKey: ['categoryDetail', slug],
    queryFn: () => catalogService.getCategoryDetail(slug),
    enabled: !!slug,
  });
}
