from .celery_app import celery_app
import asyncio
from app.db.session import async_session
from app.services.etl_service import fetch_live_odds
from app.services.understat import fetch_xg_from_understat
from app.services.football_data import fetch_matches_from_footballdata

LEAGUES = ["EPL", "La Liga", "Serie A", "Bundesliga", "Ligue 1"]

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_all_sources(self):
    async def _run():
        async with async_session() as session:
            await fetch_live_odds(session)
            for league in LEAGUES:
                await fetch_xg_from_understat(session, league)
                await fetch_matches_from_footballdata(session, league)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_run())
    except Exception as exc:
        raise self.retry(exc=exc)
