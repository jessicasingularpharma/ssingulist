// ✅ FranquiasOrdemCard.tsx
import { FC } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";

interface Franquia {
  unidade_franquia: string;
  data_compra: string;
  item: string;
  quantidade: number;
  unidade?: string;
}

interface FranquiasOrdemCardProps {
  franquias: Franquia[];
}

export const FranquiasOrdemCard: FC<FranquiasOrdemCardProps> = ({ franquias }) => {
  return (
    <Card className="bg-white shadow-md rounded-xl p-4 mt-4">
      <CardHeader>
        <h4 className="text-lg font-semibold text-gray-700">Franquias</h4>
      </CardHeader>
      <CardContent className="space-y-2">
        {franquias.length === 0 ? (
          <p className="text-gray-500">Nenhuma franquia vinculada.</p>
        ) : (
          franquias.map((f, idx) => (
            <div key={idx} className="border p-2 rounded-md">
              <p><strong>Unidade:</strong> {f.unidade_franquia}</p>
              <p><strong>Item:</strong> {f.item}</p>
              <p><strong>Quantidade:</strong> {f.quantidade} {f.unidade || ''}</p>
              <p><strong>Data da Compra:</strong> {f.data_compra}</p>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
};
