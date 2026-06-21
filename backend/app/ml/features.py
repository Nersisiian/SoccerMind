import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.match import Match
from app.db.models.odds import Odds

async def build_match_features(match_id: str, db: AsyncSession) -> pd.DataFrame:
    query = select(Match).where(Match.id == match_id)
    result = await db.execute(query)
    match = result.scalar_one_or_none()
    if not match:
        raise ValueError(f"Матч {match_id} не найден")

    home_id = match.home_team_id
    away_id = match.away_team_id

    async def _team_last_n(team_id, n=5):
        q = (
            select(Match)
            .where(
                ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
                Match.status == "finished",
            )
            .order_by(Match.kickoff.desc())
            .limit(n)
        )
        res = await db.execute(q)
        return res.scalars().all()

    home_matches = await _team_last_n(home_id)
    away_matches = await _team_last_n(away_id)

    def _avg_goals(team_id, matches):
        goals = 0
        for m in matches:
            if m.home_team_id == team_id:
                goals += m.home_score or 0
            else:
                goals += m.away_score or 0
        return goals / len(matches) if matches else 1.2

    def _avg_conceded(team_id, matches):
        conc = 0
        for m in matches:
            if m.home_team_id == team_id:
                conc += m.away_score or 0
            else:
                conc += m.home_score or 0
        return conc / len(matches) if matches else 1.0

    odds_query = select(Odds).where(Odds.match_id == match_id).order_by(Odds.timestamp.desc()).limit(1)
    odds_res = await db.execute(odds_query)
    odds = odds_res.scalar_one_or_none()

    features = {
        "home_avg_goals_last5": _avg_goals(home_id, home_matches),
        "away_avg_goals_last5": _avg_goals(away_id, away_matches),
        "home_avg_conceded_last5": _avg_conceded(home_id, home_matches),
        "away_avg_conceded_last5": _avg_conceded(away_id, away_matches),
        "odds_home_win_implied": 1.0 / odds.home_win if odds and odds.home_win else 0.45,
        "odds_draw_implied": 1.0 / odds.draw if odds and odds.draw else 0.25,
        "odds_away_win_implied": 1.0 / odds.away_win if odds and odds.away_win else 0.30,
    }

    return pd.DataFrame([features])


async def build_training_dataset(db: AsyncSession) -> pd.DataFrame:
    """Собирает признаки и целевые переменные для ВСЕХ завершённых матчей."""
    q = select(Match).where(Match.status == "finished")
    result = await db.execute(q)
    matches = result.scalars().all()

    rows = []
    for match in matches:
        try:
            feat_df = await build_match_features(str(match.id), db)
            feat = feat_df.iloc[0].to_dict()
            feat["match_id"] = str(match.id)
            feat["home_win"] = 1 if (match.home_score or 0) > (match.away_score or 0) else 0
            feat["draw"] = 1 if (match.home_score or 0) == (match.away_score or 0) else 0
            feat["away_win"] = 1 if (match.home_score or 0) < (match.away_score or 0) else 0
            feat["total_goals"] = (match.home_score or 0) + (match.away_score or 0)
            feat["btts"] = 1 if (match.home_score and match.away_score and match.home_score > 0 and match.away_score > 0) else 0
            rows.append(feat)
        except Exception:
            continue

    if not rows:
        raise ValueError("Нет завершённых матчей для обучения")

    return pd.DataFrame(rows)
