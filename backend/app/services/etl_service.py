import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.models.team import Team
from app.db.models.match import Match
from app.db.models.competition import Competition
from app.db.models.odds import Odds

async def fetch_odds(session: AsyncSession):
    if not settings.ODDS_API_KEY:
        return
    # Пример вызова The Odds API
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.the-odds-api.com/v4/sports/soccer/odds", params={"apiKey": settings.ODDS_API_KEY})
        data = resp.json()
        for game in data:
            # Обработка и сохранение
            pass