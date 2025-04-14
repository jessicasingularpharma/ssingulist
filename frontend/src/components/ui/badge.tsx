// ✅ Badge.tsx — simples componente de destaque
import React from "react";
import classNames from "classnames";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger";
}

const variantClasses = {
  default: "bg-gray-200 text-gray-800",
  success: "bg-green-200 text-green-800",
  warning: "bg-yellow-200 text-yellow-800",
  danger: "bg-red-200 text-red-800",
};

export const Badge = ({ children, variant = "default" }: BadgeProps) => {
  return (
    <span
      className={classNames(
        "inline-block px-2 py-1 text-xs font-semibold rounded-full",
        variantClasses[variant]
      )}
    >
      {children}
    </span>
  );
};
