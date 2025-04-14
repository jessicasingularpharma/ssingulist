// frontend/src/pages/MinhasSolicitacoes.tsx

import { useEffect, useState } from "react";
import api from "@/services/api";
import { Button } from "@/components/ui/button";
import classNames from "classnames";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { Clock, Check, AlertTriangle, ChevronDown, ChevronUp, Loader } from "lucide-react";

const MinhasSolicitacoes = () => {
  const [tab, setTab] = useState<"laboratorio" | "ordem_compra">("laboratorio");
  const [laboratorio, setLaboratorio] = useState<any[]>([]);
  const [ordensCompra, setOrdensCompra] = useState<any[]>([]);
  const [filtroStatus, setFiltroStatus] = useState<string>("todos");
  const [historicoStatus, setHistoricoStatus] = useState<Record<number, any[]>>({});
  const [expandido, setExpandido] = useState<number | null>(null);
  const navigate = useNavigate();

  const fetchSolicitacoes = async () => {
    try {
      const res = await api.get("/minhas-solicitacoes/");
      setLaboratorio(res.data.solicitacoes_laboratorio || []);
      setOrdensCompra(res.data.ordens_compra || []);
    } catch (err) {
      console.error("❌ Erro ao buscar solicitações:", err);
    }
  };

  const fetchHistorico = async (id: number) => {
    try {
      const res = await api.get(`/ordem-compra/${id}/historico`);
      setHistoricoStatus((prev) => ({ ...prev, [id]: res.data }));
    } catch (err) {
      console.error("Erro ao buscar histórico:", err);
    }
  };

  useEffect(() => {
    fetchSolicitacoes();
  }, []);

  const excluirSolicitacao = async (id: number, tipo: "laboratorio" | "ordem_compra") => {
    const confirmacao = confirm("Tem certeza que deseja excluir esta solicitação?");
    if (!confirmacao) return;

    try {
      if (tipo === "laboratorio") {
        await api.delete(`/solicitacoes/${id}`);
        toast.success("Solicitação de laboratório excluída!");
      } else {
        await api.delete(`/ordem-compra/deletar/${id}`);
        toast.success("Ordem de compra excluída!");
      }
      fetchSolicitacoes();
    } catch (error) {
      toast.error("Erro ao excluir a solicitação ❌");
      console.error(error);
    }
  };

  const solicitacoesAtuais = tab === "laboratorio" ? laboratorio : ordensCompra;
  const solicitacoesFiltradas = solicitacoesAtuais.filter(
    (s) => filtroStatus === "todos" || s.status === filtroStatus
  );

  const badgeVariant = (status: string) => {
    switch (status) {
      case "aberto":
        return "bg-gray-100 text-gray-700";
      case "em_andamento":
        return "bg-orange-100 text-orange-700";
      case "concluido":
        return "bg-green-100 text-green-700";
      case "em_pendencia":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-200 text-gray-700";
    }
  };

  const statusIcon = (status: string) => {
    switch (status) {
      case "aberto":
        return <Clock size={14} className="text-gray-500" />;
      case "em_andamento":
        return <Loader size={14} className="animate-spin text-orange-500" />;
      case "concluido":
        return <Check size={14} className="text-green-500" />;
      case "em_pendencia":
        return <AlertTriangle size={14} className="text-yellow-600" />;
      default:
        return <Clock size={14} className="text-gray-400" />;
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6 text-blue-700">Minhas Solicitações</h2>

      <div className="flex border-b mb-4">
        <button
          onClick={() => setTab("laboratorio")}
          className={classNames("px-4 py-2 text-sm font-medium", {
            "border-b-2 border-blue-600 text-blue-600": tab === "laboratorio",
            "text-gray-600": tab !== "laboratorio",
          })}
        >
          Solicitações Laboratório
        </button>
        <button
          onClick={() => setTab("ordem_compra")}
          className={classNames("px-4 py-2 text-sm font-medium ml-4", {
            "border-b-2 border-blue-600 text-blue-600": tab === "ordem_compra",
            "text-gray-600": tab !== "ordem_compra",
          })}
        >
          Ordens de Compra
        </button>
      </div>

      <div className="mb-4">
        <label className="mr-2 text-sm font-medium">Filtrar por status:</label>
        <select
          value={filtroStatus}
          onChange={(e) => setFiltroStatus(e.target.value)}
          className="border px-2 py-1 text-sm rounded"
        >
          <option value="todos">Todos</option>
          <option value="aberto">Aberto</option>
          <option value="em_andamento">Em andamento</option>
          <option value="em_pendencia">Em pendência</option>
          <option value="concluido">Concluído</option>
        </select>
      </div>

      {solicitacoesFiltradas.length === 0 ? (
        <p className="text-gray-500">Você ainda não enviou nenhuma solicitação.</p>
      ) : (
        <div className="space-y-4">
          {solicitacoesFiltradas.map((s) => (
            <div key={s.id} className="bg-white rounded-lg shadow-md p-4 border">
              <div className="flex justify-between items-center mb-2 flex-wrap gap-3">
                <div>
                  <p className="text-sm text-gray-500">Produtos</p>
                  <ul className="text-sm font-semibold list-disc pl-5">
                    {s.itens?.length > 0 ? (
                      s.itens.map((item: any, idx: number) => (
                        <li key={idx}>
                          {item.nome_produto} — {item.quantidade} {item.unidade}
                        </li>
                      ))
                    ) : (
                      <li className="text-gray-400">Nenhum item</li>
                    )}
                  </ul>
                </div>

                <div>
                  <p className="text-sm text-gray-500">Status</p>
                  <span className={`text-xs font-medium px-2 py-1 rounded inline-flex items-center gap-1 ${badgeVariant(s.status)}`}>
                    {statusIcon(s.status)}
                    {s.status.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase())}
                  </span>
                </div>

                <div>
                  <p className="text-sm text-gray-500">Data</p>
                  <p className="text-sm">{new Date(s.criado_em).toLocaleDateString()}</p>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="default"
                    className="text-sm"
                    onClick={() => navigate(`/solicitacoes/${tab}/${s.id}`)}
                  >
                    Ver Detalhes
                  </Button>
                  <Button
                    variant="outline"
                    className="text-red-600 border-red-300 hover:bg-red-100 hover:text-red-800"
                    onClick={() => excluirSolicitacao(s.id, tab)}
                  >
                    Excluir
                  </Button>
                </div>
              </div>

              {tab === "ordem_compra" && (
                <>
                  <button
                    className="text-sm text-blue-600 mt-2 flex items-center gap-1"
                    onClick={() => {
                      if (expandido === s.id) {
                        setExpandido(null);
                      } else {
                        setExpandido(s.id);
                        fetchHistorico(s.id);
                      }
                    }}
                  >
                    {expandido === s.id ? <ChevronUp size={16} /> : <ChevronDown size={16} />} Histórico
                  </button>
                  {expandido === s.id && historicoStatus[s.id] && (
                    <div className="mt-2 space-y-1 animate-fade-in">
                      {historicoStatus[s.id].map((h, idx) => (
                        <div key={idx} className="text-xs text-gray-700 flex items-center gap-2">
                          {statusIcon(h.status)}
                          <span className="font-semibold">
                            {h.status.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase())}
                          </span>
                          <span>em {new Date(h.data_alteracao).toLocaleString()}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MinhasSolicitacoes;
