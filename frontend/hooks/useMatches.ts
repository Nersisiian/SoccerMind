import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { Match } from '@/types';

export function useMatches() {
  return useQuery<Match[]>({
    queryKey: ['matches'],
    queryFn: async () => {
      const { data } = await api.get('/matches/');
      return data;
    },
  });
}