'use client';

import { useState } from 'react';

interface Bet {
  odds: number;
  stake: number;
  won: boolean;
}

export default function RoiCalculator() {
  const [bets, setBets] = useState<Bet[]>([{ odds: 1.5, stake: 100, won: true }]);
  const [result, setResult] = useState<{ totalProfit: number; roi: number } | null>(null);

  const addBet = () => {
    setBets([...bets, { odds: 1.5, stake: 100, won: true }]);
  };

  const updateBet = (index: number, field: keyof Bet, value: any) => {
    const updated = [...bets];
    updated[index] = { ...updated[index], [field]: value };
    setBets(updated);
  };

  const calculateRoi = () => {
    let totalStake = 0;
    let totalReturn = 0;
    for (const bet of bets) {
      totalStake += bet.stake;
      if (bet.won) {
        totalReturn += bet.stake * bet.odds;
      }
    }
    const profit = totalReturn - totalStake;
    const roi = totalStake > 0 ? (profit / totalStake) * 100 : 0;
    setResult({ totalProfit: profit, roi });
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">ROI‑калькулятор</h1>
      <div className="space-y-4">
        {bets.map((bet, idx) => (
          <div key={idx} className="flex items-center gap-4 bg-white p-4 rounded-2xl shadow">
            <input
              type="number"
              step="0.01"
              value={bet.odds}
              onChange={(e) => updateBet(idx, 'odds', parseFloat(e.target.value))}
              placeholder="Коэффициент"
              className="w-24 p-2 border rounded"
            />
            <input
              type="number"
              step="0.01"
              value={bet.stake}
              onChange={(e) => updateBet(idx, 'stake', parseFloat(e.target.value))}
              placeholder="Ставка"
              className="w-24 p-2 border rounded"
            />
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={bet.won}
                onChange={(e) => updateBet(idx, 'won', e.target.checked)}
              />
              Выиграла
            </label>
          </div>
        ))}
        <button
          onClick={addBet}
          className="px-4 py-2 bg-gray-200 rounded-full hover:bg-gray-300"
        >
          + Добавить ставку
        </button>
      </div>
      <button
        onClick={calculateRoi}
        className="mt-6 w-full py-2 bg-soccer-green text-white rounded-full hover:bg-green-700 transition"
      >
        Рассчитать ROI
      </button>
      {result && (
        <div className="mt-8 p-6 bg-white rounded-2xl shadow text-center">
          <p className="text-xl">Общая прибыль: <span className="font-bold">{result.totalProfit.toFixed(2)} €</span></p>
          <p className="text-xl">ROI: <span className="font-bold">{result.roi.toFixed(2)}%</span></p>
        </div>
      )}
    </div>
  );
}