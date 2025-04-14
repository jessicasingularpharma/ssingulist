import { useState } from "react";

const OrdemDeCompraForm = () => {
  const [itens, setItens] = useState([
    { nomeProduto: "", codigo: "", descricao: "", unidade: "", quantidade: "", urgente: false, dataNecessidade: "" }
  ]);
  const [observacao, setObservacao] = useState("");

  const handleChange = (index, field, value) => {
    const novosItens = [...itens];
    novosItens[index][field] = value;
    setItens(novosItens);
  };

  const adicionarItem = () => {
    setItens([...itens, { nomeProduto: "", codigo: "", descricao: "", unidade: "", quantidade: "", urgente: false, dataNecessidade: "" }]);
  };

  const removerItem = (index) => {
    const novosItens = itens.filter((_, i) => i !== index);
    setItens(novosItens);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Ordem de Compra:", { itens, observacao });
    // 🔁 Aqui você vai fazer o POST pro backend
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-gray-800">Abertura de Ordem de Compra</h2>

      {itens.map((item, index) => (
        <div key={index} className="border p-4 rounded space-y-4 bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Nome do Produto"
              value={item.nomeProduto}
              onChange={(e) => handleChange(index, "nomeProduto", e.target.value)}
              className="input input-bordered w-full"
              required
            />
            <input
              type="number"
              placeholder="Quantidade"
              value={item.quantidade}
              onChange={(e) => handleChange(index, "quantidade", e.target.value)}
              className="input input-bordered w-full"
              required
            />
            <input
              type="date"
              placeholder="Data de Necessidade"
              value={item.dataNecessidade}
              onChange={(e) => handleChange(index, "dataNecessidade", e.target.value)}
              className="input input-bordered w-full"
            />
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={item.urgente}
                onChange={(e) => handleChange(index, "urgente", e.target.checked)}
              />
              <span>Urgente?</span>
            </label>
          </div>

          <div className="text-sm text-gray-500">
            {/* Aqui futuramente vai exibir: Código, Descrição e Unidade puxados do banco */}
            Código: {item.codigo || "—"} | Unidade: {item.unidade || "—"} | Descrição: {item.descricao || "—"}
          </div>

          {itens.length > 1 && (
            <button
              type="button"
              onClick={() => removerItem(index)}
              className="text-red-600 hover:underline text-sm"
            >
              Remover item
            </button>
          )}
        </div>
      ))}

      <div className="space-y-2">
        <button
          type="button"
          onClick={adicionarItem}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Adicionar Produto
        </button>

        <textarea
          placeholder="Observações adicionais (opcional)"
          value={observacao}
          onChange={(e) => setObservacao(e.target.value)}
          className="textarea textarea-bordered w-full"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
      >
        Enviar Ordem de Compra
      </button>
    </form>
  );
};

export default OrdemDeCompraForm;
