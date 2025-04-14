// src/pages/GerenciarOrdens.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface OrdemCompraResumo {
  id: number;
  solicitante_nome: string;
  status: string;
  data_criacao: string;
}

const GerenciarOrdens = () => {
  const { token } = useAuth();
  const [ordens, setOrdens] = useState<OrdemCompraResumo[]>([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const fetchOrdens = async () => {
      try {
        const response = await axios.get('http://localhost:8000/ordens-compra', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setOrdens(response.data);
      } catch (error) {
        console.error('Erro ao carregar ordens:', error);
      } finally {
        setCarregando(false);
      }
    };

    fetchOrdens();
  }, [token]);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-blue-700">Gerenciar Ordens de Compra</h1>

      {carregando ? (
        <p>Carregando ordens...</p>
      ) : ordens.length === 0 ? (
        <p className="text-gray-500">Nenhuma ordem encontrada.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {ordens.map((ordem) => (
            <Card key={ordem.id} className="shadow border border-gray-200">
              <CardContent className="p-4 space-y-2">
                <p className="text-sm text-gray-500">ID: {ordem.id}</p>
                <h2 className="text-lg font-semibold">Solicitante: {ordem.solicitante_nome}</h2>
                <p>Status: <span className="font-medium text-blue-700">{ordem.status}</span></p>
                <p className="text-sm text-gray-600">Criado em: {new Date(ordem.data_criacao).toLocaleDateString()}</p>
                <Button variant="outline" onClick={() => alert(`Ver detalhes da ordem ${ordem.id}`)}>
                  Ver Detalhes
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default GerenciarOrdens;