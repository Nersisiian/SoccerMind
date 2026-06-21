import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.db.models.team import Team
from app.db.models.match import Match
from app.db.models.competition import Competition
from app.db.models.odds import Odds
from datetime import datetime, timezone
import uuid

logger = logging.getLogger(__name__)

LEAGUE_MAP = {
    "soccer_epl": "EPL",
    "soccer_spain_la_liga": "La Liga",
    "soccer_italy_serie_a": "Serie A",
    "soccer_germany_bundesliga": "Bundesliga",
    "soccer_france_ligue_one": "Ligue 1",
}

async def fetch_live_odds(db: AsyncSession):
    if not settings.ODDS_API_KEY:
        logger.warning("ODDS_API_KEY not set")
        return

    base_url = "https://api.the-odds-api.com/v4/sports"
    for sport_key in LEAGUE_MAP.keys():
        params = {
            "apiKey": settings.ODDS_API_KEY,
            "regions": "eu",
            "markets": "h2h",
            "oddsFormat": "decimal",
            "dateFormat": "iso",
        }
        url = f"{base_url}/{sport_key}/odds/"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params, timeout=30.0)
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Odds API error for {sport_key}: {e.response.status_code}")
                continue
            except Exception as e:
                logger.error(f"Odds API network error: {e}")
                continue

        for game in data:
            home_team = await _get_or_create_team(db, game["home_team"])
            away_team = await _get_or_create_team(db, game["away_team"])

            competition_name = LEAGUE_MAP.get(game.get("sport_key"), game.get("sport_title", "Unknown"))
            competition = await _get_or_create_competition(db, competition_name)

            match_external_id = game.get("id")
            match = await db.scalar(select(Match).where(Match.external_id == match_external_id))
            if not match:
                match = Match(
                    id=uuid.uuid4(),
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    competition_id=competition.id,
                    kickoff=datetime.fromisoformat(game["commence_time"]),
                    status="scheduled",
                    external_id=match_external_id,
                )
                db.add(match)
                await db.flush()

            for bookmaker in game.get("bookmakers", []):
                bookmaker_name = bookmaker["title"]
                for market in bookmaker.get("markets", []):
                    if market["key"] == "h2h":
                        outcomes = {o["name"]: o["price"] for o in market["outcomes"]}
                        home_win = outcomes.get(home_team.name, None)
                        away_win = outcomes.get(away_team.name, None)
                        draw = outcomes.get("Draw", None)

                        existing_odds = await db.scalar(
                            select(Odds).where(
                                Odds.match_id == match.id,
                                Odds.bookmaker == bookmaker_name,
                                Odds.market == "h2h",
                            )
                        )
                        if existing_odds:
                            existing_odds.home_win = home_win
                            existing_odds.draw = draw
                            existing_odds.away_win = away_win
                            existing_odds.timestamp = datetime.now(timezone.utc)
                        else:
                            odds_entry = Odds(
                                match_id=match.id,
                                bookmaker=bookmaker_name,
                                market="h2h",
                                home_win=home_win,
                                draw=draw,
                                away_win=away_win,
                            )
                            db.add(odds_entry)

            await db.commit()
            logger.info(f"Odds saved for {home_team.name} vs {away_team.name}")

    logger.info("Live odds collection finished.")

async def _get_or_create_team(db: AsyncSession, team_name: str) -> Team:
    result = await db.execute(select(Team).where(Team.name == team_name))
    team = result.scalar_one_or_none()
    if not team:
        team = Team(id=uuid.uuid4(), name=team_name)
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
