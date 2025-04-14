import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

interface Solicitacao {
  id: number;
  usuario_nome: string;
  produto: string;
  quantidade: number;
  status: string;
  criado_em: string;
}

const DetalhesSolicitacao = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [solicitacao, setSolicitacao] = useState<Solicitacao | null>(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    const fetchSolicitacao = async () => {
      if (!id) {
        setErro("ID da solicitação inválido.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`http://localhost:8000/solicitacoes/${id}`);
        setSolicitacao(response.data);
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          setErro(error.response?.data?.detail || "Erro ao buscar detalhes da solicitação.");
        } else {
          setErro("Erro inesperado.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchSolicitacao();
  }, [id]);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "aprovado":
        return "text-green-600";
      case "pendente":
        return "text-yellow-600";
      case "rejeitado":
        return "text-red-600";
      default:
        return "text-gray-700";
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center mt-20 text-blue-700 animate-pulse">
        <svg className="w-10 h-10 mb-3 animate-spin text-blue-600" fill="none" viewBox="0 0 24 24">
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
          />
        </svg>
        <p className="text-sm">Carregando detalhes da solicitação...</p>
      </div>
    );
  }

  if (erro) {
    return <p className="text-center mt-10 text-red-600 font-medium">{erro}</p>;
  }

  if (!solicitacao) return null;

  return (
    <div className="max-w-xl mx-auto mt-12 p-6 bg-white rounded-xl shadow space-y-5 animate-fade-in">
      <h2 className="text-2xl font-bold text-blue-700">
        Detalhes da Solicitação #{solicitacao.id}
      </h2>

      <hr className="border-t border-gray-300" />

      <p><strong>Usuário:</strong> {solicitacao.usuario_nome}</p>
      <p><strong>Produto:</strong> {solicitacao.produto}</p>
      <p><strong>Quantidade:</strong> {solicitacao.quantidade}</p>
      <p>
        <strong>Status:</strong>{" "}
        <span className={`font-semibold ${getStatusColor(solicitacao.status)}`}>
          {solicitacao.status}
        </span>
      </p>
      <p>
        <strong>Data de criação:</strong>{" "}
        {new Date(solicitacao.criado_em).toLocaleString("pt-BR")}
      </p>

      <button
        onClick={() => navigate("/solicitacoes")}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition duration-200"
      >
        Voltar para Minhas Solicitações
      </button>
    </div>
  );
};

export default DetalhesSolicitacao;
