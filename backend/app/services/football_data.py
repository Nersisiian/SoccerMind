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
    "EPL": "PL",
    "La Liga": "PD",
    "Serie A": "SA",
    "Bundesliga": "BL1",
    "Ligue 1": "FL1",
}

async def fetch_matches_from_footballdata(db: AsyncSession, league: str = "EPL"):
    if not settings.FOOTBALL_DATA_API_KEY:
        return
    code = LEAGUE_CODES.get(league)
    if not code:
        return
    headers = {"X-Auth-Token": settings.FOOTBALL_DATA_API_KEY}
    url = f"{BASE_URL}/competitions/{code}/matches?limit=50"
    await _process_matches(url, headers, db, league)

async def fetch_historical_matches(db: AsyncSession, league: str, season: str):
    if not settings.FOOTBALL_DATA_API_KEY:
        return
    code = LEAGUE_CODES.get(league)
    if not code:
        return
    headers = {"X-Auth-Token": settings.FOOTBALL_DATA_API_KEY}
    url = f"{BASE_URL}/competitions/{code}/matches?status=FINISHED&limit=500&season={season}"
    await _process_matches(url, headers, db, league)

async def _process_matches(url, headers, db, league):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, timeout=60.0)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"Football-Data error: {e}")
            return
    if "matches" not in data:
        return
    for match_data in data["matches"]:
        home_name = match_data["homeTeam"]["name"]
        away_name = match_data["awayTeam"]["name"]
        home_team = await _get_or_create_team(db, home_name)
        away_team = await _get_or_create_team(db, away_name)
        comp_name = match_data.get("competition", {}).get("name", league)
        competition = await _get_or_create_competition(db, comp_name)
        kickoff = datetime.fromisoformat(match_data["utcDate"])
        status = "finished" if match_data["status"] == "FINISHED" else "scheduled"
        match_id = match_data.get("id")
        match = await db.scalar(select(Match).where(Match.external_id == str(match_id)))
        if match:
            if status == "finished":
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
                status="finished" if status == "finished" else "scheduled",
                external_id=str(match_id),
                home_score=match_data["score"]["fullTime"]["home"] if status == "finished" else None,
                away_score=match_data["score"]["fullTime"]["away"] if status == "finished" else None,
            )
            db.add(match)
    await db.commit()
    logger.info(f"Matches for {league} updated.")

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
