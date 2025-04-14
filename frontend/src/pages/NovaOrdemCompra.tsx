import { useState } from "react";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";
import { Usuario } from "../types/AuthTypes";
import api from "@/services/api";
import { Button } from "@/components/ui/button"; // ✅ import do botão estilizado

interface SugestaoProduto {
  codigo: number;
  descricao: string;
  unidade: string;
}

interface ProdutoItem {
  nome: string;
  quantidade: number;
  observacao: string;
  dataNecessidade: string;
  urgente: boolean;
  codigo: number | null;
  unidade: string;
  sugestoes: SugestaoProduto[];
}

const NovaOrdemCompra = () => {
  const { user } = useAuth();

  const [itens, setItens] = useState<ProdutoItem[]>([
    {
      nome: "",
      quantidade: 1,
      observacao: "",
      dataNecessidade: "",
      urgente: false,
      codigo: null,
      unidade: "",
      sugestoes: [],
    },
  ]);

  const buscarProdutos = async (query: string): Promise<SugestaoProduto[]> => {
    if (query.length < 2) return [];
    try {
      const response = await api.get(`/produtos/buscar?nome=${query}`);
      return response.data;
    } catch (error) {
      console.error("❌ Erro ao buscar produtos:", error);
      return [];
    }
  };

  const atualizarItem = <K extends keyof ProdutoItem>(
    index: number,
    campo: K,
    valor: ProdutoItem[K]
  ) => {
    const novosItens = [...itens];
    novosItens[index][campo] = valor;
    setItens(novosItens);
  };

  const adicionarItem = () => {
    setItens([
      ...itens,
      {
        nome: "",
        quantidade: 1,
        observacao: "",
        dataNecessidade: "",
        urgente: false,
        codigo: null,
        unidade: "",
        sugestoes: [],
      },
    ]);
  };

  const removerItem = (index: number) => {
    setItens((prev) => prev.filter((_, i) => i !== index));
  };

  const enviarOrdem = async () => {
    if (!user?.id) {
      alert("Usuário não autenticado.");
      return;
    }

    const payload = {
      solicitante_id: user.id,
      itens: itens.map((item) => ({
        codigo_produto: item.codigo!,
        nome_produto: item.nome,
        quantidade: item.quantidade,
        unidade: item.unidade,
        observacao: item.observacao || null,
        data_necessidade: item.dataNecessidade || null,
        urgente: item.urgente,
      })),
    };

    try {
      const response = await axios.post("http://localhost:8000/ordem-compra/criar", payload);
      alert("✅ Ordem de compra enviada com sucesso!");
      console.log(response.data);

      setItens([
        {
          nome: "",
          quantidade: 1,
          observacao: "",
          dataNecessidade: "",
          urgente: false,
          codigo: null,
          unidade: "",
          sugestoes: [],
        },
      ]);
    } catch (error) {
      console.error("❌ Erro ao enviar ordem:", error);
      alert("Erro ao enviar ordem de compra. Verifique os dados.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded shadow space-y-6">
      <h2 className="text-2xl font-semibold text-blue-700">Nova Ordem de Compra</h2>

      {itens.map((item, index) => (
        <div
          key={index}
          className="grid md:grid-cols-2 gap-4 bg-gray-50 p-4 rounded border relative"
        >
          <div>
            <label className="block text-sm text-gray-600">Nome do Produto *</label>
            <input
              type="text"
              className="input"
              value={item.nome}
              onChange={async (e) => {
                const valor = e.target.value;
                atualizarItem(index, "nome", valor);
                const sugestoes = await buscarProdutos(valor);
                atualizarItem(index, "sugestoes", sugestoes);
              }}
              required
            />
            {item.sugestoes.length > 0 && (
              <ul className="absolute z-10 bg-white border w-full mt-1 rounded shadow max-h-48 overflow-auto">
                {item.sugestoes.map((produto) => (
                  <li
                    key={produto.codigo}
                    onClick={() => {
                      atualizarItem(index, "nome", produto.descricao);
                      atualizarItem(index, "codigo", produto.codigo);
                      atualizarItem(index, "unidade", produto.unidade);
                      atualizarItem(index, "sugestoes", []);
                    }}
                    className="p-2 hover:bg-blue-100 cursor-pointer"
                  >
                    {produto.descricao} ({produto.unidade})
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div>
            <label className="block text-sm text-gray-600">Quantidade *</label>
            <input
              type="number"
              min={1}
              className="input"
              value={item.quantidade}
              onChange={(e) =>
                atualizarItem(index, "quantidade", parseInt(e.target.value) || 1)
              }
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600">Código do Produto</label>
            <input
              type="text"
              className="input bg-gray-100"
              value={item.codigo ?? ""}
              readOnly
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600">Unidade</label>
            <input
              type="text"
              className="input bg-gray-100"
              value={item.unidade}
              readOnly
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600">Data de Necessidade</label>
            <input
              type="date"
              className="input"
              value={item.dataNecessidade}
              onChange={(e) => atualizarItem(index, "dataNecessidade", e.target.value)}
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm text-gray-600">Urgente?</label>
            <input
              type="checkbox"
              checked={item.urgente}
              onChange={(e) => atualizarItem(index, "urgente", e.target.checked)}
              className="mt-2"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm text-gray-600">Observações</label>
            <textarea
              className="input"
              value={item.observacao}
              onChange={(e) => atualizarItem(index, "observacao", e.target.value)}
              rows={2}
            />
          </div>

          <div className="md:col-span-2 flex justify-end">
            {itens.length > 1 && (
              <Button
              variant="outline"
              className="text-red-600 border-red-500 hover:bg-red-100 text-sm"
              onClick={() => removerItem(index)}
            >
              Remover Item
            </Button>
            
            )}
          </div>
        </div>
      ))}

      <div className="flex gap-4 justify-end">
        <Button
          variant="outline"
          onClick={adicionarItem}
        >
          + Adicionar Item
        </Button>

        <Button
          onClick={enviarOrdem}
        >
          Enviar Ordem
        </Button>
      </div>
    </div>
  );
};

export default NovaOrdemCompra;
