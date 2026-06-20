'use client';
import { useRoi } from '@/hooks/useRoi';
import RoiChart from '@/components/RoiChart';

export default function AnalyticsPage() {
  const { data: roi, isLoading } = useRoi();
  if (isLoading) return <p>Загрузка...</p>;
  if (!roi) return <p>Нет данных</p>;
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Аналитика</h1>
      <RoiChart roi={roi} />
    </div>
  );
}
