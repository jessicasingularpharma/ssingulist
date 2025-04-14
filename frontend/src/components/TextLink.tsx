import React, { AnchorHTMLAttributes, ReactNode } from 'react';

interface TextLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  children: ReactNode;
  className?: string;
}

export const TextLink = ({ children, className = '', ...props }: TextLinkProps) => (
  <a
    {...props}
    className={`text-blue-600 hover:text-blue-700 hover:underline transition-colors ${className}`}
  >
    {children}
  </a>
);
