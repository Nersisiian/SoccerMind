'use client';

import { useParams } from 'next/navigation';
import useSWR from 'swr';
import { fetcher } from '@/services/api';
import { MatchDetail } from '@/types';
import PredictionChart from '@/components/PredictionChart';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function MatchDetailPage() {
  const params = useParams<{ id: string }>();
  const { id } = params;
  const { data: match, error } = useSWR<MatchDetail>(id ? `/matches/${id}` : null, fetcher);

  if (error) return <div className="text-center mt-10 text-red-500">Ошибка загрузки</div>;
  if (!match) return <div className="text-center mt-10">Загрузка...</div>;

  const scoreDistribution = match.predictions?.[0]?.predicted_score
    ? Object.entries(match.predictions[0].predicted_score).map(([score, prob]) => ({
        score,
        prob: Math.round(Number(prob) * 100),
      }))
    : [];

  return (
    <div className="container mx-auto p-4 max-w-5xl">
      <h1 className="text-3xl font-bold mb-2">{match.home_team.name} vs {match.away_team.name}</h1>
      <p className="text-gray-600">{new Date(match.kickoff).toLocaleString()} — {match.status}</p>
      {match.home_score !== null && match.away_score !== null && (
        <div className="text-4xl font-bold mt-4">{match.home_score} - {match.away_score}</div>
      )}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        {match.predictions && match.predictions.length > 0 && (
          <PredictionChart prediction={match.predictions[0]} />
        )}
        {match.odds && match.odds.length > 0 && (
          <div className="bg-white p-4 rounded-2xl shadow">
            <h3 className="text-xl font-bold mb-4">Коэффициенты</h3>
            {match.odds.map((odd: any) => (
              <div key={odd.bookmaker} className="flex justify-between border-b py-2">
                <span className="font-medium">{odd.bookmaker}</span>
                <span>{odd.home_win?.toFixed(2)} / {odd.draw?.toFixed(2)} / {odd.away_win?.toFixed(2)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      {scoreDistribution.length > 0 && (
        <div className="mt-8 bg-white p-4 rounded-2xl shadow">
          <h3 className="text-xl font-bold mb-4">Распределение точного счёта</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={scoreDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="score" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="prob" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}