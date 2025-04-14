export interface Usuario {
  id: number;
  codigo_funcionario: number;
  nome: string;
  email?: string;
  is_admin: boolean;
}

export interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  user: Usuario | null;
  loading: boolean;
  login: (codigo_funcionario: number, senha: string) => Promise<boolean>;
  logout: () => void;
}
