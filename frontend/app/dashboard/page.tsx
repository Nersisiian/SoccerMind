'use client';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DashboardPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login');
    }
  }, [status, router]);

  if (status === 'loading') return <p>Загрузка...</p>;
  if (!session) return null;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Личный кабинет</h1>
      <div className="bg-white p-6 rounded-2xl shadow">
        <p className="text-lg">Email: {session.user?.email}</p>
        <p className="text-lg">Роль: {session.user?.role ?? 'Неизвестно'}</p>
        <p className="text-lg mt-4">Управление подпиской (скоро)</p>
      </div>
    </div>
  );
}
