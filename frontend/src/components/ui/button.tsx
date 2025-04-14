import { ReactNode, ButtonHTMLAttributes } from "react";
import clsx from "clsx";

type Variant = "default" | "danger" | "success" | "outline";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: Variant;
  className?: string;
}

export const Button = ({ children, variant = "default", className, ...props }: ButtonProps) => {
  const variantStyles = {
    default: "bg-blue-600 hover:bg-blue-700 text-white",
    danger: "bg-red-600 hover:bg-red-700 text-white",
    success: "bg-green-600 hover:bg-green-700 text-white",
    outline: "border border-gray-300 text-gray-700 hover:bg-gray-100",
  };

  return (
    <button
      className={clsx("px-4 py-2 rounded-lg text-sm font-medium transition", variantStyles[variant], className)}
      {...props}
    >
      {children}
    </button>
  );
};
