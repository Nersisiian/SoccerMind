import { RoiData } from '@/types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function RoiChart({ roi }: { roi: RoiData }) {
  const data = [
    { name: 'ROI %', value: roi.roi_percent },
    { name: 'Ставок', value: roi.total_bets },
    { name: 'Выигрышей', value: roi.wins },
  ];
  return (
    <div className="bg-white p-4 rounded-2xl shadow">
      <h2 className="text-xl font-bold mb-4">ROI статистика</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#10B981" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}