import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const Input = ({ className = '', ...props }: InputProps) => (
  <input
    {...props}
    className={`block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm 
    placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 
    focus:border-blue-500 sm:text-sm ${className}`}
  />
);
