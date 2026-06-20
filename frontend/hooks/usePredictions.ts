import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { Prediction } from '@/types';

export function usePredictions() {
  return useQuery<Prediction[]>({
    queryKey: ['predictions'],
    queryFn: async () => {
      const { data } = await api.get('/predictions/daily');
      return data;
    },
  });
}
