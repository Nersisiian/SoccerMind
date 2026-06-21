from .celery_app import celery_app
import asyncio
from app.db.session import async_session
from app.ml.predict import predict_match
from app.db.models.match import Match
from app.db.models.prediction import Prediction
from sqlalchemy import select
from datetime import datetime, timezone

@celery_app.task
def generate_upcoming_predictions():
    async def _run():
        async with async_session() as session:
            query = select(Match).where(
                Match.kickoff >= datetime.now(timezone.utc),
                Match.status == "scheduled"
            )
            result = await session.execute(query)
            matches = result.scalars().all()
            for match in matches:
                try:
                    pred_data = await predict_match(str(match.id), session)
                    prediction = Prediction(
                        match_id=match.id,
                        model_version="1.0.0",
                        predicted_home_win=pred_data["home_win"],
                        predicted_draw=pred_data["draw"],
                        predicted_away_win=pred_data["away_win"],
                        predicted_over_2_5=pred_data["over2.5"],
                        predicted_btts=pred_data["btts"],
                        predicted_score=pred_data.get("score_distribution"),
                    )
                    session.add(prediction)
                except Exception as e:
                    print(f"Ошибка прогноза для {match.id}: {e}")
            await session.commit()
    asyncio.get_event_loop().run_until_complete(_run())
