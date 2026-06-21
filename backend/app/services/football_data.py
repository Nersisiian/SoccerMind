import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.db.models.team import Team
from app.db.models.match import Match
from app.db.models.competition import Competition
from datetime import datetime, timezone
import uuid

logger = logging.getLogger(__name__)

BASE_URL = "https://api.football-data.org/v4"

LEAGUE_CODES = {
    "Английская Премьер‑лига": "PL",
    "Ла Лига": "PD",
    "Серия А": "SA",
    "Бундеслига": "BL1",
    "Лига 1": "FL1",
}

async def fetch_matches_from_footballdata(db: AsyncSession, league: str = "Английская Премьер‑лига"):
    """Загружает завершённые и предстоящие матчи из Football-Data.org."""
    if not settings.FOOTBALL_DATA_API_KEY:
        logger.warning("FOOTBALL_DATA_API_KEY не задан – пропускаем Football-Data.org.")
        return

    league_code = LEAGUE_CODES.get(league)
    if not league_code:
        logger.warning(f"Лига {league} не найдена в маппинге Football-Data.")
        return

    headers = {"X-Auth-Token": settings.FOOTBALL_DATA_API_KEY}
    
    # Запрашиваем и завершённые, и запланированные матчи (без фильтра статуса)
    url = f"{BASE_URL}/competitions/{league_code}/matches?limit=50"

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, timeout=30.0)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"Ошибка Football-Data.org: {e}")
            return

    if "matches" not in data:
        logger.warning("Нет поля 'matches' в ответе Football-Data.")
        return

    for match_data in data["matches"]:
        home_name = match_data["homeTeam"]["name"]
        away_name = match_data["awayTeam"]["name"]

        home_team = await _get_or_create_team(db, home_name)
        away_team = await _get_or_create_team(db, away_name)

        comp_name = match_data.get("competition", {}).get("name", league)
        competition = await _get_or_create_competition(db, comp_name)

        kickoff = datetime.fromisoformat(match_data["utcDate"])
        status = match_data["status"]  # FINISHED, SCHEDULED, LIVE, etc.

        match_id = match_data.get("id")
        match = await db.scalar(select(Match).where(Match.external_id == str(match_id)))
        if match:
            # Обновляем результат, если есть
            if status == "FINISHED":
                match.home_score = match_data["score"]["fullTime"]["home"]
                match.away_score = match_data["score"]["fullTime"]["away"]
                match.status = "finished"
        else:
            match = Match(
                id=uuid.uuid4(),
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                competition_id=competition.id,
                kickoff=kickoff,
                status="finished" if status == "FINISHED" else "scheduled",
                external_id=str(match_id),
                home_score=match_data["score"]["fullTime"]["home"] if status == "FINISHED" else None,
                away_score=match_data["score"]["fullTime"]["away"] if status == "FINISHED" else None,
            )
            db.add(match)

    await db.commit()
    logger.info(f"Football-Data.org: матчи для лиги {league} обновлены (всего {len(data['matches'])} матчей).")


async def _get_or_create_team(db: AsyncSession, name: str) -> Team:
    result = await db.execute(select(Team).where(Team.name == name))
    team = result.scalar_one_or_none()
    if not team:
        team = Team(id=uuid.uuid4(), name=name)
        db.add(team)
        await db.flush()
    return team

async def _get_or_create_competition(db: AsyncSession, name: str) -> Competition:
    result = await db.execute(select(Competition).where(Competition.name == name))
    comp = result.scalar_one_or_none()
    if not comp:
        comp = Competition(id=uuid.uuid4(), name=name)
        db.add(comp)
        await db.flush()
    return comp
