import { Prediction } from '@/types';
import { PieChart, Pie, Cell, Legend } from 'recharts';

const COLORS = ['#10B981', '#F59E0B', '#EF4444'];

export default function PredictionChart({ prediction }: { prediction: Prediction }) {
  const data = [
    { name: 'Хозяева', value: prediction.predicted_home_win },
    { name: 'Ничья', value: prediction.predicted_draw },
    { name: 'Гости', value: prediction.predicted_away_win },
  ];
  return (
    <div className="bg-white p-4 rounded-2xl shadow">
      <h2 className="text-xl font-bold mb-2">
        {prediction.match.home_team.name} vs {prediction.match.away_team.name}
      </h2>
      <div className="flex justify-between items-center">
        <PieChart width={200} height={200}>
          <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={80} dataKey="value">
            {data.map((entry, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Legend />
        </PieChart>
        <div>
          <p>Обе забьют: {(prediction.predicted_btts * 100).toFixed(0)}%</p>
          <p>Тотал &gt;2.5: {(prediction.predicted_over_2_5 * 100).toFixed(0)}%</p>
        </div>
      </div>
    </div>
  );
}