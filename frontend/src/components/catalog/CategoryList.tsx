'use client';

import { cn } from '../../lib/utils';
import { Category } from '../../types';
import { Skeleton } from '../ui/Skeleton';

interface CategoryListProps {
  categories?: Category[];
  isLoading?: boolean;
  activeSlug?: string | null;
  onSelect: (slug: string | null) => void;
}

export function CategoryList({ categories, isLoading, activeSlug, onSelect }: CategoryListProps) {
  if (isLoading) {
    return (
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-9 w-24 rounded-full shrink-0" />
        ))}
      </div>
    );
  }

  return (
    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
      <button
        onClick={() => onSelect(null)}
        className={cn(
          'px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap shrink-0',
          activeSlug === null
            ? 'bg-violet-600 text-white shadow-md shadow-violet-200'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        )}
      >
        All
      </button>
      {categories?.map((cat) => (
        <button
          key={cat.id}
          onClick={() => onSelect(cat.slug)}
          className={cn(
            'px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap shrink-0',
            activeSlug === cat.slug
              ? 'bg-violet-600 text-white shadow-md shadow-violet-200'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          )}
        >
          {cat.name}
        </button>
      ))}
    </div>
  );
}
