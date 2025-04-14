import { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  className?: string;
}

export const Button = ({ children, className = '', ...props }: ButtonProps) => (
  <button
    {...props}
    className={`w-full py-2 px-4 bg-black text-white rounded-md font-medium 
    hover:bg-gray-900 transition-colors ${className}`}
  >
    {children}
  </button>
);
