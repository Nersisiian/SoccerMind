from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.match import Match
from app.db.models.prediction import Prediction
from app.db.models.user import User
from app.ml.predict import predict_match
from datetime import datetime, timezone
from app.schemas.prediction import PredictionFilter

class PredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_daily_predictions(self, user: User, filters: PredictionFilter):
        # Проверка подписки: бесплатные пользователи видят только прогнозы с задержкой 24ч
        # Для упрощения возвращаем все прогнозы на сегодня
        now = datetime.now(timezone.utc)
        query = select(Prediction).join(Match).where(Match.kickoff >= now)
        if filters.league:
            query = query.where(Match.competition.has(name=filters.league))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_prediction_history(self, user: User, filters: PredictionFilter):
        query = select(Prediction).join(Match).where(Match.status == "finished")
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_matches(self, league: str = None):
        query = select(Match).options(selectinload(Match.home_team), selectinload(Match.away_team)).where(Match.kickoff >= datetime.now(timezone.utc))
        if league:
            query = query.where(Match.competition.has(name=league))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_match_detail(self, match_id: str):
        query = select(Match).options(selectinload(Match.home_team), selectinload(Match.away_team), selectinload(Match.odds), selectinload(Match.predictions)).where(Match.id == match_id)
        result = await self.db.execute(query)
        match = result.scalar_one_or_none()
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        return match

    async def get_roi(self, user: User):
        # Заглушка ROI статистики
        return {"roi_percent": 12.5, "total_bets": 100, "wins": 55}