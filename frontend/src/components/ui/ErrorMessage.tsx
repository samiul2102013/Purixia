import * as React from 'react';
import { AlertCircle } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ErrorMessageProps extends React.HTMLAttributes<HTMLDivElement> {
  message: string;
}

export function ErrorMessage({ message, className, ...props }: ErrorMessageProps) {
  return (
    <div
      className={cn(
        'flex items-center gap-3 p-4 bg-red-50 border border-red-200/60 rounded-xl text-sm text-red-700',
        className
      )}
      role="alert"
      {...props}
    >
      <AlertCircle className="w-5 h-5 shrink-0 text-red-500" />
      <span className="font-medium">{message}</span>
    </div>
  );
}
