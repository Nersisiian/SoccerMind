'use client';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';

export default function Navbar() {
  const { data: session } = useSession();
  return (
    <nav className="bg-soccer-dark text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold">
          SoccerMind AI
        </Link>
        <div className="space-x-4">
          <Link href="/matches">Матчи</Link>
          <Link href="/predictions">Прогнозы</Link>
          <Link href="/analytics">Аналитика</Link>
          {session ? (
            <>
              <Link href="/dashboard">Кабинет</Link>
              <button onClick={() => signOut()} className="text-red-400 hover:text-red-300">
                Выйти
              </button>
            </>
          ) : (
            <Link href="/login">Войти</Link>
          )}
        </div>
      </div>
    </nav>
  );
}