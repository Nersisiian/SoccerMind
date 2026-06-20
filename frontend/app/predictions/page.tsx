'use client';
import { usePredictions } from '@/hooks/usePredictions';
import PredictionChart from '@/components/PredictionChart';

export default function PredictionsPage() {
  const { data: predictions, isLoading } = usePredictions();
  if (isLoading) return <p>Загрузка прогнозов...</p>;
  if (!predictions || predictions.length === 0) return <p>Прогнозов пока нет</p>;
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">AI Прогнозы</h1>
      <div className="space-y-8">
        {predictions.map((p) => (
          <PredictionChart key={p.id} prediction={p} />
        ))}
      </div>
    </div>
  );
}
