import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { jwtDecode as jwt_decode } from 'jwt-decode';
import { AuthContextType, Usuario } from '../types/AuthTypes';

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [user, setUser] = useState<Usuario | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verificar = async () => {
      if (token) {
        await carregarUsuario(token);
      }
      setLoading(false);
    };
    verificar();
  }, [token]);

  const carregarUsuario = async (token: string) => {
    try {
      const decoded: any = jwt_decode(token);

      console.log("🔐 Token decodificado:", decoded); // ✅ Ajuda a debug

      setUser({
        id: parseInt(decoded.sub), // `sub` é o ID do usuário
        codigo_funcionario: decoded.codigo_funcionario, // agora está correto
        nome: decoded.nome || "",
        email: decoded.email || "",
        is_admin: decoded.is_admin,
      });

      setIsAuthenticated(true);
    } catch (error) {
      console.error("🚫 Erro ao decodificar token:", error);
      logout();
    }
  };

  const login = async (codigo_funcionario: number, senha: string) => {
    try {
      const response = await axios.post("http://localhost:8000/login", {
        codigo_funcionario,
        senha,
      });

      const accessToken = response.data.access_token;
      localStorage.setItem("token", accessToken);
      setToken(accessToken); // ✅ dispara carregamento do usuário
      return true;
    } catch (error) {
      console.error("❌ Erro ao fazer login:", error);
      setLoading(false);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth deve ser usado dentro de um AuthProvider");
  return context;
};
