from .celery_app import celery_app
import asyncio
from app.db.session import async_session
from app.ml.train import train_models

@celery_app.task
def retrain_models():
    async def _run():
        async with async_session() as session:
            await train_models(session)
    asyncio.get_event_loop().run_until_complete(_run())