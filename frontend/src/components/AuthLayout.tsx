interface AuthLayoutProps {
    children: React.ReactNode;
  }
  
  export const AuthLayout = ({ children }: AuthLayoutProps) => (
    <div className="min-h-screen flex items-center justify-center bg-white px-4">
      <div className="w-full max-w-md space-y-8">{children}</div>
    </div>
  );
  