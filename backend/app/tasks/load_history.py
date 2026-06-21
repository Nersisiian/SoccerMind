from .celery_app import celery_app
import asyncio
from app.db.session import async_session
from app.services.football_data import fetch_historical_matches
from app.services.understat import fetch_xg_from_understat

@celery_app.task(bind=True, max_retries=3)
def load_historical_data(self):
    seasons = ["2023"]
    async def _run():
        async with async_session() as session:
            for season in seasons:
                await fetch_historical_matches(session, "EPL", season)
                await fetch_xg_from_understat(session, "EPL", season)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_run())
        return f"Loaded seasons: {seasons}"
    except Exception as exc:
        raise self.retry(exc=exc)
