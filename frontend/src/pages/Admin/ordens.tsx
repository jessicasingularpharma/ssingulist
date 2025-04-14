// src/pages/Admin/ListaOrdens.tsx
import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

interface OrdemCompra {
  id: number;
  solicitante_nome: string;
  status: string;
  data_criacao: string;
}

const ListaOrdens = () => {
  const [ordens, setOrdens] = useState<OrdemCompra[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrdens = async () => {
      try {
        const response = await axios.get("http://localhost:8000/ordens-compra/todas");
        setOrdens(response.data);
      } catch (error) {
        console.error("Erro ao buscar ordens:", error);
      }
    };

    fetchOrdens();
  }, []);

  return (
    <div className="max-w-6xl mx-auto py-10 px-6">
      <h1 className="text-3xl font-bold text-blue-700 mb-8">Painel de Ordens de Compra</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {ordens.map((ordem) => (
          <div
            key={ordem.id}
            className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition duration-300 cursor-pointer"
            onClick={() => navigate(`/admin/ordens/${ordem.id}`)}
          >
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Ordem #{ordem.id}</h2>
            <p className="text-sm text-gray-600">Solicitante: <span className="font-medium">{ordem.solicitante_nome}</span></p>
            <p className="text-sm text-gray-600">Status: <span className={`font-semibold ${ordem.status === 'finalizado' ? 'text-green-600' : ordem.status === 'em andamento' ? 'text-yellow-600' : 'text-red-600'}`}>{ordem.status}</span></p>
            <p className="text-sm text-gray-600">Criado em: <span className="font-medium">{new Date(ordem.data_criacao).toLocaleDateString()}</span></p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ListaOrdens;
