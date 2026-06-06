import { useQuery } from '@tanstack/react-query';
import { bannerService } from '../services/banners';

export function useBanners() {
  return useQuery({
    queryKey: ['banners'],
    queryFn: bannerService.getBanners,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}
