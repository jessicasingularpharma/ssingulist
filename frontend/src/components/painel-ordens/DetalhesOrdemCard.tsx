// ✅ DetalhesOrdemCard.tsx
import { FC } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";

interface DetalhesOrdemCardProps {
  detalhes: {
    data_compra?: string;
    previsao_chegada?: string;
    fornecedor?: string;
    observacao_geral?: string;
  };
}

export const DetalhesOrdemCard: FC<DetalhesOrdemCardProps> = ({ detalhes }) => {
  return (
    <Card className="bg-white shadow-md rounded-xl p-4">
      <CardHeader>
        <h4 className="text-lg font-semibold text-gray-700">Detalhes da Compra</h4>
      </CardHeader>
      <CardContent className="space-y-2">
        <p><strong>Data da Compra:</strong> {detalhes.data_compra || "Não informada"}</p>
        <p><strong>Previsão de Chegada:</strong> {detalhes.previsao_chegada || "Não informada"}</p>
        <p><strong>Fornecedor:</strong> {detalhes.fornecedor || "Não informado"}</p>
        <p><strong>Observação:</strong> {detalhes.observacao_geral || "-"}</p>
      </CardContent>
    </Card>
  );
};
// ... código anterior do DetalhesOrdemCard (sem alterações) ...

// 🔹 Novo componente: PendenciasSubstanciaCard
export const PendenciasSubstanciaCard: FC<{ pendencias: any[] }> = ({ pendencias }) => {
  return (
    <Card className="bg-gray-50 shadow rounded-xl p-4">
      <CardHeader>
        <h4 className="text-lg font-semibold text-gray-700">Pendências de Substâncias</h4>
      </CardHeader>
      <CardContent className="space-y-2">
        {pendencias.length > 0 ? (
          pendencias.map((pendencia, idx) => (
            <div key={idx} className="text-sm text-gray-800">
              <p><strong>Situação:</strong> {pendencia.situacao}</p>
              <p><strong>Localização:</strong> {pendencia.localizacao}</p>
              <p><strong>Status:</strong> {pendencia.status}</p>
              <hr className="my-2 border-gray-200" />
            </div>
          ))
        ) : (
          <p className="text-gray-500">Nenhuma pendência registrada.</p>
        )}
      </CardContent>
    </Card>
  );
};

// 🔹 Novo componente: FranquiasOrdemCard
export const FranquiasOrdemCard: FC<{ franquias: any[] }> = ({ franquias }) => {
  return (
    <Card className="bg-gray-50 shadow rounded-xl p-4">
      <CardHeader>
        <h4 className="text-lg font-semibold text-gray-700">Franquias</h4>
      </CardHeader>
      <CardContent className="space-y-2">
        {franquias.length > 0 ? (
          franquias.map((franquia, idx) => (
            <div key={idx} className="text-sm text-gray-800">
              <p><strong>Unidade:</strong> {franquia.unidade_franquia}</p>
              <p><strong>Data da Compra:</strong> {franquia.data_compra}</p>
              <p><strong>Item:</strong> {franquia.item}</p>
              <p><strong>Quantidade:</strong> {franquia.quantidade} {franquia.unidade}</p>
              <hr className="my-2 border-gray-200" />
            </div>
          ))
        ) : (
          <p className="text-gray-500">Nenhuma franquia registrada.</p>
        )}
      </CardContent>
    </Card>
  );
};


