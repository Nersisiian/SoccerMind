from .celery_app import celery_app
from app.services.etl_service import fetch_odds

@celery_app.task(bind=True, max_retries=3)
def fetch_all_sources(self):
    # В реальной системе используем асинхронную сессию, здесь синхронный вариант
    # Так как Celery не поддерживает async напрямую, используем asyncio.run
    import asyncio
    from app.db.session import async_session
    async def _run():
        async with async_session() as session:
            await fetch_odds(session)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run())