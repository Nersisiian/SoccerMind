import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.match import Match
from app.db.models.team import Team

async def build_match_features(match_id: str, db: AsyncSession) -> pd.DataFrame:
    query = select(Match).where(Match.id == match_id)
    result = await db.execute(query)
    match = result.scalar_one_or_none()
    if not match:
        raise ValueError("Match not found")

    home_team = match.home_team
    away_team = match.away_team

    # Простые признаки для демонстрации
    features = {
        "home_team_id": str(home_team.id),
        "away_team_id": str(away_team.id),
        "hour": match.kickoff.hour,
        "day_of_week": match.kickoff.weekday(),
    }

    # Добавляем исторические данные (заглушка: средние значения)
    features["home_avg_goals_last5"] = 1.5
    features["away_avg_goals_last5"] = 1.2
    features["home_xg_avg_last5"] = 1.8
    features["away_xg_avg_last5"] = 1.4
    features["odds_home_win_implied"] = 0.45
    features["odds_draw_implied"] = 0.25
    features["odds_away_win_implied"] = 0.30

    return pd.DataFrame([features])