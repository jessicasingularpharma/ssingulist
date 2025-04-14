import { ReactNode } from "react";
import clsx from "clsx";

export const Card = ({ children, className }: { children: ReactNode; className?: string }) => {
  return (
    <div
      className={clsx(
        "rounded-2xl bg-white shadow-md border border-gray-200 overflow-hidden",
        className
      )}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className }: { children: ReactNode; className?: string }) => {
  return (
    <div className={clsx("px-6 py-4 border-b border-gray-200 font-semibold text-lg", className)}>
      {children}
    </div>
  );
};

export const CardContent = ({ children, className }: { children: ReactNode; className?: string }) => {
  return <div className={clsx("px-6 py-4", className)}>{children}</div>;
};

export const CardFooter = ({ children, className }: { children: ReactNode; className?: string }) => {
  return <div className={clsx("px-6 py-4 border-t border-gray-200", className)}>{children}</div>;
};
