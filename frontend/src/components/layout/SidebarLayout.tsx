// frontend/src/components/layouts/SidebarLayout.tsx

import { useState, useEffect, useMemo } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { Menu, X, LogOut } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const SidebarLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const [carregando, setCarregando] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (user !== null) {
      setCarregando(false);
    }
  }, [user]);

  const navigation = useMemo(() => {
    const baseLinks = [
      { name: 'Dashboard', href: '/dashboard' },
      { name: 'Minhas Solicitações', href: '/solicitacoes' },
      { name: 'Solicitação Laboratório', href: '/solicitacoes-laboratorio/nova' },
      { name: 'Nova Ordem de Compra', href: '/ordem-compra/nova' },
      { name: 'Alterar Senha', href: '/alterar-senha' },
    ];

    if (user?.is_admin) {
      baseLinks.push({ name: 'Gerenciamento', href: '/ordens-compra/gerenciar' });
      baseLinks.push({ name: 'Criar Usuário', href: '/cadastro' });
    }

    return baseLinks;
  }, [user]);

  if (carregando || !isAuthenticated || !user) {
    return (
      <div className="h-screen flex items-center justify-center text-gray-600">
        Carregando informações do usuário...
      </div>
    );
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 z-40 w-64 bg-white shadow-lg transition-transform transform ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } md:translate-x-0 md:static`}
      >
        <div className="p-4 border-b font-bold text-xl text-blue-700">
          Sistema de Gestão Integrada
        </div>
        <div className="px-4 py-2 text-sm text-gray-600">
          Olá, <span className="font-semibold">{user.nome || user.codigo_funcionario}</span>
        </div>
        <nav className="p-4 space-y-2">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className="block px-4 py-2 rounded hover:bg-blue-100 text-gray-800"
              onClick={() => setSidebarOpen(false)}
            >
              {item.name}
            </Link>
          ))}
        </nav>
        <div className="p-4">
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-100 rounded w-full"
          >
            <LogOut size={16} /> Sair
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col w-full">
        {/* Topbar mobile */}
        <div className="flex items-center justify-between p-4 border-b shadow-sm md:hidden bg-white">
          <button onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <h1 className="text-lg font-semibold text-blue-700">Suprimentos</h1>
        </div>

        <main className="flex-1 overflow-y-auto p-6 bg-gray-50">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default SidebarLayout;
