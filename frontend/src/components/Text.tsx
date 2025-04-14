import { AnchorHTMLAttributes, ReactNode } from 'react';

export const Text = ({ children, className = '' }: { children: ReactNode; className?: string }) => (
  <p className={`text-sm text-gray-600 ${className}`}>{children}</p>
);

export const TextLink = ({
  children,
  className = '',
  ...props
}: AnchorHTMLAttributes<HTMLAnchorElement>) => (
  <a className={`text-blue-600 hover:text-blue-700 hover:underline transition-colors ${className}`} {...props}>
    {children}
  </a>
);

export const Strong = ({ children }: { children: ReactNode }) => (
  <strong className="font-semibold text-gray-900">{children}</strong>
);
