import { getSession } from 'next-auth/react';

export async function getCurrentUser() {
  const session = await getSession();
  return session?.user;
}

export async function getAuthToken(): Promise<string | null> {
  const session = await getSession();
  return (session as any)?.accessToken || null;
}
