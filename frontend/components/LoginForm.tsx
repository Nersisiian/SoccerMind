'use client';
import { useState, FormEvent } from 'react';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
  error: string;
}

export default function LoginForm({ onSubmit, error }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(email, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <div>
        <label className="block text-sm font-medium">Email</label>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mt-1 p-2 border rounded-lg"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Пароль</label>
        <input
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mt-1 p-2 border rounded-lg"
        />
      </div>
      <button type="submit" className="w-full py-2 bg-soccer-green text-white rounded-lg hover:bg-green-700 transition">
        Войти
      </button>
    </form>
  );
}