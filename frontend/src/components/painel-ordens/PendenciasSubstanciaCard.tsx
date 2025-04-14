// ✅ PendenciasSubstanciaCard.tsx
import { FC } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";

interface Pendencia {
  situacao: string;
  localizacao?: string;
  status: string;
}

interface PendenciasSubstanciaCardProps {
  pendencias: Pendencia[];
}

export const PendenciasSubstanciaCard: FC<PendenciasSubstanciaCardProps> = ({ pendencias }) => {
  return (
    <Card className="bg-white shadow-md rounded-xl p-4 mt-4">
      <CardHeader>
        <h4 className="text-lg font-semibold text-gray-700">Pendências de Substâncias</h4>
      </CardHeader>
      <CardContent className="space-y-2">
        {pendencias.length === 0 ? (
          <p className="text-gray-500">Nenhuma pendência registrada.</p>
        ) : (
          pendencias.map((p, idx) => (
            <div key={idx} className="border p-2 rounded-md">
              <p><strong>Situação:</strong> {p.situacao}</p>
              <p><strong>Localização:</strong> {p.localizacao || '-'}</p>
              <p><strong>Status:</strong> {p.status}</p>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
};