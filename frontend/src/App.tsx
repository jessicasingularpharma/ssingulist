// ✅ App.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Cadastro from './pages/cadastro';
import AlterarSenha from './pages/AlterarSenha';
import Dashboard from './pages/Dashboard';
import NovaOrdemDeCompra from './pages/NovaOrdemCompra';
import PainelGerenciarOrdensCompra from './pages/PainelGerenciarOrdensCompra';
import Pendencias from './pages/Pendencias';
import Franquias from './pages/Franquias';
import GerenciarPlanilha from './pages/GerenciarPlanilha';
import SidebarLayout from './components/layout/SidebarLayout';
import PrivateRoute from './components/PrivateRoute';
import RequireAdmin from './components/RequireAdmin';
import NovaSolicitacaoLaboratorio from '@/pages/NovaSolicitacaoLaboratorio';
import MinhasSolicitacoes from '@/pages/MinhasSolicitacoes'; // ✅ Import da nova tela

function App() {
  return (
    <Routes>
      {/* Rotas públicas */}
      <Route path="/login" element={<Login />} />
      <Route path="/alterar-senha" element={<AlterarSenha />} />
      <Route path="/gerenciar" element={<GerenciarPlanilha />} />
      <Route path="/pendencias" element={<Pendencias />} />
      <Route path="/franquias" element={<Franquias />} />

      {/* Rota protegida apenas para admins */}
      <Route
        path="/cadastro"
        element={
          <PrivateRoute>
            <RequireAdmin>
              <Cadastro />
            </RequireAdmin>
          </PrivateRoute>
        }
      />

      {/* Rotas privadas com layout lateral */}
      <Route
        element={
          <PrivateRoute>
            <SidebarLayout />
          </PrivateRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/ordem-compra/nova" element={<NovaOrdemDeCompra />} />
        <Route path="/solicitacoes" element={<MinhasSolicitacoes />} /> {/* ✅ Nova rota */}
        <Route
          path="/ordens-compra/gerenciar"
          element={
            <RequireAdmin>
              <PainelGerenciarOrdensCompra />
            </RequireAdmin>
          }
        />
        <Route
          path="/solicitacoes-laboratorio/nova"
          element={<NovaSolicitacaoLaboratorio />}
        />
      </Route>

      {/* Redirecionamento padrão */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
