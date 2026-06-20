'use client';
import { useMatches } from '@/hooks/useMatches';
import MatchCard from '@/components/MatchCard';

export default function MatchesPage() {
  const { data: matches, isLoading, error } = useMatches();
  if (isLoading) return <p>Загрузка...</p>;
  if (error) return <p className="text-red-500">Ошибка загрузки матчей</p>;
  if (!matches) return <p>Нет матчей</p>;
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Матчи</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {matches.map((match) => (
          <MatchCard key={match.id} match={match} />
        ))}
      </div>
    </div>
  );
}
