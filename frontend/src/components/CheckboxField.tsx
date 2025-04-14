import React, { ReactNode } from 'react';

interface CheckboxFieldProps {
  children: ReactNode;
  className?: string;
}

export const CheckboxField = ({ children, className = '' }: CheckboxFieldProps) => (
  <div className={`flex items-center gap-2 ${className}`}>{children}</div>
);
