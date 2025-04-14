import { useAuth } from "@/contexts/AuthContext";
import { Navigate } from "react-router-dom";

import { ReactNode } from "react";

const RequireAdmin = ({ children }: { children: ReactNode }) => {
  const { user } = useAuth();

  if (!user?.is_admin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default RequireAdmin;
