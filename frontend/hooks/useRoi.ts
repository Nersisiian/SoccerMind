import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { RoiData } from '@/types';

export function useRoi() {
  return useQuery<RoiData>({
    queryKey: ['roi'],
    queryFn: async () => {
      const { data } = await api.get('/analytics/roi');
      return data;
    },
  });
}