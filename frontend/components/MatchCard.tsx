import { Match } from '@/types';

export default function MatchCard({ match }: { match: Match }) {
  return (
    <div className="bg-white p-4 rounded-2xl shadow hover:shadow-lg transition">
      <div className="flex justify-between items-center">
        <span className="font-semibold">{match.home_team.name}</span>
        <span className="text-gray-500">vs</span>
        <span className="font-semibold">{match.away_team.name}</span>
      </div>
      <div className="text-sm text-gray-600 mt-2">
        {new Date(match.kickoff).toLocaleString()}
      </div>
      {match.home_score !== null && match.away_score !== null && (
        <div className="text-center mt-2 text-xl font-bold">
          {match.home_score} - {match.away_score}
        </div>
      )}
    </div>
  );
}