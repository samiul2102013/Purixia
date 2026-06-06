import * as React from 'react';
import { cn } from '../../lib/utils';
import { OrderStatus } from '../../types';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  status?: OrderStatus | 'in_stock' | 'out_of_stock';
  size?: 'sm' | 'md';
}

export function Badge({ className, status = 'pending', size = 'sm', children, ...props }: BadgeProps) {
  
  const statusColors = {
    pending: 'bg-amber-50 text-amber-700 border-amber-200/60',
    confirmed: 'bg-blue-50 text-blue-700 border-blue-200/60',
    shipped: 'bg-purple-50 text-purple-700 border-purple-200/60',
    delivered: 'bg-green-50 text-green-700 border-green-200/60',
    cancelled: 'bg-red-50 text-red-700 border-red-200/60',
    in_stock: 'bg-emerald-50 text-emerald-700 border-emerald-200/60',
    out_of_stock: 'bg-rose-50 text-rose-700 border-rose-200/60',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-[10px] font-bold rounded-md uppercase tracking-wider border',
    md: 'px-2.5 py-1 text-xs font-semibold rounded-lg uppercase tracking-wide border',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center justify-center font-medium select-none',
        statusColors[status] || 'bg-gray-100 text-gray-800 border-gray-200',
        sizes[size],
        className
      )}
      {...props}
    >
      {children || status.replace('_', ' ')}
    </span>
  );
}
