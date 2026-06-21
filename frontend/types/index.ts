export interface Team {
  id: string;
  name: string;
  country?: string;
}

export interface Match {
  id: string;
  home_team: Team;
  away_team: Team;
  kickoff: string;
  status: string;
  home_score: number | null;
  away_score: number | null;
}

export interface Prediction {
  id: string;
  match: Match;
  model_version: string;
  predicted_home_win: number;
  predicted_draw: number;
  predicted_away_win: number;
  predicted_over_2_5: number;
  predicted_btts: number;
  predicted_score: Record<string, number>;
}

export interface RoiData {
  roi_percent: number;
  total_bets: number;
  wins: number;
}
export interface MatchDetail extends Match { odds: any[]; predictions: any[]; }
