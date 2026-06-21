'use client';
import { useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import api from '@/services/api';

const plans = [
  { id: 'monthly', name: 'Ежемесячная', price: '€9.99/мес', priceId: 'price_monthly_id' },
  { id: 'yearly', name: 'Годовая', price: '€99.99/год', priceId: 'price_yearly_id' },
];

export default function SubscribePage() {
  const { data: session } = useSession();
  const router = useRouter();
  const [loading, setLoading] = useState<string | null>(null);

  if (!session) {
    return <p className="text-center mt-10">Пожалуйста, войдите в систему.</p>;
  }

  const handleSubscribe = async (priceId: string) => {
    setLoading(priceId);
    try {
      const { data } = await api.post('/payments/create-checkout-session', { price_id: priceId });
      window.location.href = data.url;
    } catch (err) {
      alert('Ошибка при создании сессии оплаты');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6 text-center">Выберите план подписки</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {plans.map((plan) => (
          <div key={plan.id} className="border rounded-2xl p-6 shadow hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-2">{plan.name}</h2>
            <p className="text-xl mb-4">{plan.price}</p>
            <button
              onClick={() => handleSubscribe(plan.priceId)}
              disabled={loading === plan.priceId}
              className="w-full py-2 bg-soccer-green text-white rounded-full hover:bg-green-700 transition disabled:opacity-50"
            >
              {loading === plan.priceId ? 'Загрузка...' : 'Оформить'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
