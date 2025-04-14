import { useState, ChangeEvent } from "react";
import api from "@/services/api";
import { useAuth } from "@/contexts/AuthContext";
import Input from "@/components/ui/Input";
import { Button } from "@/components/ui/button";
import toast from "react-hot-toast";
import { PlusCircle, Trash2 } from "lucide-react";

interface SugestaoProduto {
  codigo: number;
  descricao: string;
  unidade: string;
}

const NovaSolicitacaoLaboratorio = () => {
  const { user } = useAuth();
  const [produtos, setProdutos] = useState([
    { codigo_produto: "", nome_produto: "", quantidade: "", unidade: "" },
  ]);
  const [sugestoes, setSugestoes] = useState<SugestaoProduto[][]>([]);

  const handleChange = (index: number, field: string, value: string) => {
    const novosProdutos = [...produtos];
    novosProdutos[index][field as keyof typeof novosProdutos[0]] = value;
    setProdutos(novosProdutos);
  };

  const adicionarProduto = () => {
    setProdutos([
      ...produtos,
      { codigo_produto: "", nome_produto: "", quantidade: "", unidade: "" },
    ]);
    setSugestoes([...sugestoes, []]);
  };

  const removerProduto = (index: number) => {
    const novosProdutos = produtos.filter((_, i) => i !== index);
    const novasSugestoes = sugestoes.filter((_, i) => i !== index);
    setProdutos(novosProdutos);
    setSugestoes(novasSugestoes);
  };

  const buscarProdutos = async (index: number, query: string) => {
    if (query.length < 2) return;

    try {
      const response = await api.get(`/produtos/buscar?nome=${query}`);
      const novasSugestoes = [...sugestoes];
      novasSugestoes[index] = response.data;
      setSugestoes(novasSugestoes);
    } catch (error) {
      console.error("❌ Erro ao buscar produto:", error);
    }
  };

  const enviarSolicitacao = async () => {
    try {
      const payload = {
        itens: produtos.map((p) => ({
          codigo_produto: parseInt(p.codigo_produto),
          nome_produto: p.nome_produto,
          quantidade: parseInt(p.quantidade),
          unidade: p.unidade,
          urgente: false,
        })),
      };
  
      await api.post("/solicitacoes", payload);
      toast.success("✅ Solicitação enviada!");
      setProdutos([{ codigo_produto: "", nome_produto: "", quantidade: "", unidade: "" }]);
    } catch (error) {
      toast.error("❌ Erro ao enviar solicitação");
      console.error(error);
    }
  };  

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6 text-blue-700">
        Nova Solicitação - Laboratório
      </h2>

      <div className="space-y-4">
        {produtos.map((produto, index) => (
          <div key={index} className="border rounded-lg p-4 bg-white shadow-sm relative">
            <div className="grid grid-cols-4 gap-4">
              <div className="col-span-2 relative">
                <Input
                  label="Nome"
                  name="nome_produto"
                  value={produto.nome_produto}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => {
                    const valor = e.target.value;
                    handleChange(index, "nome_produto", valor);
                    buscarProdutos(index, valor);
                  }}
                  placeholder="Nome do Produto"
                />
                {Array.isArray(sugestoes[index]) && sugestoes[index].length > 0 && (
                  <ul className="absolute bg-white border rounded shadow z-10 w-full mt-1 max-h-48 overflow-y-auto">
                    {sugestoes[index].map((sugestao) => (
                      <li
                        key={sugestao.codigo}
                        className="px-3 py-2 hover:bg-blue-100 cursor-pointer"
                        onClick={() => {
                          const novosProdutos = [...produtos];
                          novosProdutos[index].codigo_produto = sugestao.codigo.toString();
                          novosProdutos[index].nome_produto = sugestao.descricao;
                          novosProdutos[index].unidade = sugestao.unidade;
                          setProdutos(novosProdutos);
                          const novasSugestoes = [...sugestoes];
                          novasSugestoes[index] = [];
                          setSugestoes(novasSugestoes);
                        }}
                      >
                        {sugestao.descricao} ({sugestao.codigo}) - {sugestao.unidade}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <Input
                label="Código"
                name="codigo_produto"
                value={produto.codigo_produto}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(index, "codigo_produto", e.target.value)
                }
                placeholder="Código"
              />
              <Input
                label="Qtd"
                name="quantidade"
                value={produto.quantidade}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(index, "quantidade", e.target.value)
                }
                placeholder="Quantidade"
              />
              <Input
                label="Unidade"
                name="unidade"
                value={produto.unidade}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(index, "unidade", e.target.value)
                }
                placeholder="Un"
              />
            </div>

            {produtos.length > 1 && (
              <div className="mt-4 flex justify-end">
                <Button
                  variant="outline"
                  className="text-red-600 border-red-500 hover:bg-red-100"
                  onClick={() => removerProduto(index)}
                >
                  <Trash2 size={16} className="mr-2" /> Remover Produto
                </Button>
              </div>
            )}
          </div>
        ))}

        <div className="flex gap-4 mt-6">
          <Button variant="outline" onClick={adicionarProduto}>
            <PlusCircle className="mr-2" size={16} /> Adicionar Produto
          </Button>
          <Button onClick={enviarSolicitacao}>Enviar Solicitação</Button>
        </div>
      </div>
    </div>
  );
};

export default NovaSolicitacaoLaboratorio;
