'use client';

import * as React from 'react';
import { motion } from 'framer-motion';

interface PageWrapperProps {
  children: React.ReactNode;
  className?: string;
}

export function PageWrapper({ children, className }: PageWrapperProps) {
  return (
    <motion.main
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: 'easeOut' }}
      className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 ${className || ''}`}
    >
      {children}
    </motion.main>
  );
}
