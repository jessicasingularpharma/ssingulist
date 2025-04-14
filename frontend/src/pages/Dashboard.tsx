import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dialog } from '@headlessui/react';

import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/Button';
import { Heading } from '@/components/Heading';
import { Text } from '@/components/Text';
console.log("DASHBOARD FOI RENDERIZADA");

const Dashboard = () => {
  const [mostrarPopup, setMostrarPopup] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();

  // Verifica se o usuário já alterou a senha
  useEffect(() => {
    const jaAlterouSenha = localStorage.getItem('senha_alterada') === 'true';
    setMostrarPopup(!jaAlterouSenha);
  }, []);

  const irParaAlterarSenha = () => {
    setMostrarPopup(false);
    navigate('/alterar-senha');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-100 space-y-6 p-4">
      <Heading className="text-2xl">Bem-vindo {user?.nome}!</Heading>

      <Text>Este é o painel inicial do sistema de controle de suprimentos.</Text>


      {/* Pop-up de alteração de senha */}
      <Dialog open={mostrarPopup} onClose={() => setMostrarPopup(false)} className="relative z-50">
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="w-full max-w-md bg-white p-6 rounded-xl shadow space-y-4">
            <Dialog.Title className="text-xl font-semibold">
              Deseja alterar sua senha agora?
            </Dialog.Title>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setMostrarPopup(false)}
                className="px-4 py-2 rounded bg-gray-100 text-gray-700 hover:bg-gray-200"
              >
                Agora não
              </button>
              <button
                onClick={irParaAlterarSenha}
                className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
              >
                Alterar senha
              </button>
            </div>
          </Dialog.Panel>
        </div>
      </Dialog>
    </div>
  );
};

export default Dashboard;
