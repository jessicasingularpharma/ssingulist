// frontend/src/pages/PainelGerenciarOrdensCompra.tsx
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "@/contexts/AuthContext";
import Input from "@/components/ui/Input";
import { Button } from "@/components/ui/button";
import { CheckCircle, XCircle, ChevronDown, ChevronUp, Clock, Check, AlertTriangle, Loader } from "lucide-react";
import classNames from "classnames";

const PainelGerenciarOrdensCompra = () => {
  const { token } = useAuth();
  const [tab, setTab] = useState<"suprimentos" | "laboratorio">("suprimentos");
  const [ordens, setOrdens] = useState<any[]>([]);
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);
  const [ordemAberta, setOrdemAberta] = useState<number | null>(null);
  const [historicoStatus, setHistoricoStatus] = useState<Record<number, any[]>>({});

  useEffect(() => {
    const fetchOrdens = async () => {
      try {
        const res = await axios.get("http://localhost:8000/ordem-compra/listar-todas", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setOrdens(res.data);
      } catch (err) {
        console.error("Erro ao carregar ordens de compra:", err);
      }
    };
    fetchOrdens();
  }, [token]);

  const handleUpdate = async (ordem: any) => {
    try {
      await axios.put(
        `http://localhost:8000/ordem-compra/atualizar-detalhes/${ordem.id}`,
        ordem.detalhes,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      await axios.put(
        `http://localhost:8000/ordem-compra/atualizar-status/${ordem.id}`,
        { status: ordem.status },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMensagem(`Ordem ${ordem.identificador} salva com sucesso! ✅`);
      setTimeout(() => setMensagem(null), 3000);
    } catch (error) {
      console.error("Erro ao atualizar detalhes ou status:", error);
      setMensagemErro("Erro ao salvar ordem. Tente novamente.");
      setTimeout(() => setMensagemErro(null), 4000);
    }
  };
  const handleStatusChange = async (ordemId: number, novoStatus: string) => {
    try {
      await axios.put(
        `http://localhost:8000/ordem-compra/atualizar-status/${ordemId}`,
        { status: novoStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setOrdens((prev) =>
        prev.map((ordem) =>
          ordem.id === ordemId ? { ...ordem, status: novoStatus } : ordem
        )
      );
      setMensagem(`Status da ordem alterado para "${novoStatus.replace("_", " ")}"`);
      fetchHistoricoStatus(ordemId); // Recarrega o histórico atualizado
      setTimeout(() => setMensagem(null), 3000);
    } catch (error) {
      console.error("Erro ao alterar status:", error);
      setMensagemErro("Erro ao alterar status. Tente novamente.");
      setTimeout(() => setMensagemErro(null), 4000);
    }
  };  
  const handleInputChange = (ordemId: number, field: string, value: string) => {
    setOrdens((prev) =>
      prev.map((o) =>
        o.id === ordemId
          ? {
              ...o,
              detalhes: {
                ...o.detalhes,
                [field]: value,
              },
            }
          : o
      )
    );
  };

  const fetchHistoricoStatus = async (ordemId: number) => {
    if (historicoStatus[ordemId]) return;
    try {
      const res = await axios.get(`http://localhost:8000/ordem-compra/${ordemId}/historico`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setHistoricoStatus((prev) => ({ ...prev, [ordemId]: res.data }));
    } catch (error) {
      console.error("Erro ao buscar histórico de status:", error);
    }
  };

  const ordensFiltradas = ordens.filter((ordem) =>
    tab === "suprimentos" ? ordem.tipo === "suprimentos" : ordem.tipo === "laboratorio"
  );

  const renderIconeStatus = (status: string) => {
    switch (status) {
      case "aberto": return <Clock size={16} className="text-yellow-500" />;
      case "em_andamento": return <Loader size={16} className="text-blue-500 animate-spin" />;
      case "em_pendencia": return <AlertTriangle size={16} className="text-orange-500" />;
      case "concluido": return <Check size={16} className="text-green-600" />;
      default: return <Clock size={16} className="text-gray-400" />;
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-blue-700">Painel de Gerenciamento</h2>

      <div className="flex border-b gap-4">
        <button
          onClick={() => setTab("suprimentos")}
          className={classNames("px-4 py-2 text-sm font-medium", {
            "border-b-2 border-blue-600 text-blue-600": tab === "suprimentos",
            "text-gray-600": tab !== "suprimentos",
          })}
        >
          Suprimentos
        </button>
        <button
          onClick={() => setTab("laboratorio")}
          className={classNames("px-4 py-2 text-sm font-medium", {
            "border-b-2 border-blue-600 text-blue-600": tab === "laboratorio",
            "text-gray-600": tab !== "laboratorio",
          })}
        >
          Laboratório
        </button>
      </div>

      {mensagem && (
        <div className="flex items-center gap-2 bg-green-100 text-green-800 border border-green-300 px-4 py-2 rounded shadow-sm animate-fade-in">
          <CheckCircle size={20} /> <span>{mensagem}</span>
        </div>
      )}

      {mensagemErro && (
        <div className="flex items-center gap-2 bg-red-100 text-red-800 border border-red-300 px-4 py-2 rounded shadow-sm animate-fade-in">
          <XCircle size={20} /> <span>{mensagemErro}</span>
        </div>
      )}

      <div className="space-y-4">
        {ordensFiltradas.map((ordem) => (
          <div key={ordem.id} className="bg-white shadow-md rounded-lg border">
            <button
              className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-gray-50 transition"
              onClick={async () => {
                const nova = ordemAberta === ordem.id ? null : ordem.id;
                setOrdemAberta(nova);
                if (nova) await fetchHistoricoStatus(ordem.id);
              }}
            >
              <div className="space-y-2">
  <p className="text-sm font-semibold">Alterar Status</p>
  <div className="flex gap-2 flex-wrap">
    <Button variant="outline" onClick={() => handleStatusChange(ordem.id, "aberto")}>Aberto</Button>
    <Button variant="outline" onClick={() => handleStatusChange(ordem.id, "em_andamento")}>Em Andamento</Button>
    <Button variant="outline" onClick={() => handleStatusChange(ordem.id, "em_pendencia")}>Em Pendência</Button>
    <Button variant="outline" onClick={() => handleStatusChange(ordem.id, "concluido")}>Concluído</Button>
  </div>
</div>

              <div>
                <h3 className="text-blue-700 font-semibold">{ordem.identificador}</h3>
                <p className="text-sm text-gray-600">
                  Solicitante: <strong>{ordem.solicitante?.nome || ordem.solicitante?.codigo_funcionario}</strong>
                </p>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm bg-gray-100 px-2 py-1 rounded text-gray-800">
                  {ordem.status.replace("_", " ").replace(/\b\w/g, (l: string) => l.toUpperCase())}
                </span>
                {ordemAberta === ordem.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </div>
            </button>

            {ordemAberta === ordem.id && (
              <div className="px-4 pb-4 animate-fade-in space-y-4">
                <div className="py-2 border-t">
                  <p className="font-semibold mb-1">Itens da Ordem</p>
                  <ul className="text-sm text-gray-700 list-disc ml-4">
                    {ordem.itens?.map((item: any, idx: number) => (
                      <li key={idx}>
                        {item.nome_produto} — {item.quantidade} {item.unidade}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Input label="Data da Compra" name="data_compra" type="date" value={ordem.detalhes?.data_compra?.slice(0, 10) || ""} onChange={(e: { target: { value: string; }; }) => handleInputChange(ordem.id, "data_compra", e.target.value)} placeholder={undefined} />
                  <Input label="Fornecedor" name="fornecedor" value={ordem.detalhes?.fornecedor || ""} onChange={(e: { target: { value: string; }; }) => handleInputChange(ordem.id, "fornecedor", e.target.value)} placeholder={undefined} />
                  <Input label="Observações" name="observacao_geral" value={ordem.detalhes?.observacao_geral || ""} onChange={(e: { target: { value: string; }; }) => handleInputChange(ordem.id, "observacao_geral", e.target.value)} placeholder={undefined} />
                </div>

                <div className="text-sm bg-gray-50 border rounded p-3">
                  <p className="font-semibold mb-2">Histórico de Status</p>
                  <ul className="space-y-2">
                    {(historicoStatus[ordem.id] || []).map((h, idx) => (
                      <li key={idx} className="flex items-center gap-2 text-gray-800">
                        {renderIconeStatus(h.status)}
                        <span className="font-medium capitalize">{h.status.replace("_", " ")}</span>
                        <span className="text-xs text-gray-500 ml-auto">
                          {new Date(h.data_alteracao).toLocaleString("pt-BR")}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex justify-end">
                  <Button onClick={() => handleUpdate(ordem)}>Salvar</Button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PainelGerenciarOrdensCompra;
