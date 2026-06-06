import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { ApiError } from '../types';
import axios from 'axios';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: string | number): string {
  const numericPrice = typeof price === 'string' ? parseFloat(price) : price;
  if (isNaN(numericPrice)) return '৳ 0.00';
  return `৳ ${numericPrice.toFixed(2)}`;
}

export function formatDate(dateString: string): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function getImageUrl(path: string | null): string {
  if (!path) return '/images/placeholder.png';
  
  // If it's already a full URL, return it
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }

  // Get base URL from env or fallback to localhost
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || (typeof window !== 'undefined' ? 'http://localhost:8000' : 'http://127.0.0.1:8000');
  
  // Ensure we don't double slash or have issues with the path
  const cleanBase = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  
  // If the path already contains the base URL (sometimes DRF does this depending on config)
  if (path.includes('://')) return path;

  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBase}${cleanPath}`;
}

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const apiError = error.response?.data as ApiError | undefined;
    if (apiError) {
      if (apiError.detail) return apiError.detail;
      if (apiError.error) return apiError.error;
      if (apiError.non_field_errors && apiError.non_field_errors.length > 0) {
        return apiError.non_field_errors[0];
      }
      // Check for first field error
      const keys = Object.keys(apiError);
      for (const key of keys) {
        if (key !== 'detail' && key !== 'error' && key !== 'non_field_errors') {
          const val = apiError[key];
          if (Array.isArray(val) && val.length > 0) {
            return `${key}: ${val[0]}`;
          } else if (typeof val === 'string') {
            return `${key}: ${val}`;
          }
        }
      }
    }
    return error.message || 'An error occurred with the network request.';
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'Something went wrong. Try again.';
}
