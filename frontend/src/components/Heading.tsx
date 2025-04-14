import { ReactNode } from 'react';

export const Heading = ({ children, className = '' }: { children: ReactNode; className?: string }) => (
  <h2 className={`text-2xl font-semibold text-gray-900 ${className}`}>{children}</h2>
);
