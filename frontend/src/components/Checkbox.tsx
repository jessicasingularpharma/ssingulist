import { InputHTMLAttributes, ReactNode } from 'react';

export const Checkbox = (props: InputHTMLAttributes<HTMLInputElement>) => (
  <input
    type="checkbox"
    className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
    {...props}
  />
);

export const CheckboxField = ({ children }: { children: ReactNode }) => (
  <div className="flex items-center gap-2">{children}</div>
);
