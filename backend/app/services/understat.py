import logging
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.team import Team
from app.db.models.match import Match
from app.db.models.competition import Competition
from datetime import datetime, timezone
import asyncio
import re

logger = logging.getLogger(__name__)

BASE_URL = "https://understat.com/league/"

LEAGUE_ID_MAP = {
    "Английская Премьер‑лига": "EPL",
    "Ла Лига": "La_liga",
    "Серия А": "Serie_A",
    "Бундеслига": "Bundesliga",
    "Лига 1": "Ligue_1",
}

async def fetch_xg_from_understat(db: AsyncSession, league_name: str = "Английская Премьер‑лига"):
    """Скачивает страницу лиги Understat, парсит матчи и сохраняет xG."""
    league_id = LEAGUE_ID_MAP.get(league_name)
    if not league_id:
        logger.warning(f"Лига {league_name} не найдена в маппинге Understat.")
        return

    url = f"{BASE_URL}{league_id}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=30.0)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
        except Exception as e:
            logger.error(f"Ошибка загрузки Understat: {e}")
            return

    # Ищем скрипт с данными
    scripts = soup.find_all("script")
    data_script = None
    for script in scripts:
        if "datesData" in script.text:
            data_script = script.text
            break
    if not data_script:
        logger.warning("Не найден JSON с данными матчей на Understat.")
        return

    # Извлекаем JSON из JavaScript
    match = re.search(r"datesData\s*=\s*'([^']+)'", data_script)
    if not match:
        match = re.search(r'datesData\s*=\s*"(.*)"', data_script)
    if not match:
        logger.warning("Не удалось извлечь JSON datesData.")
        return

    import json
    data = json.loads(match.group(1))

    # Обработка матчей
    for date_str, matches_list in data.items():
        for match_data in matches_list:
            home_name = match_data["h"]["title"]
            away_name = match_data["a"]["title"]

            home_team = await _get_or_create_team(db, home_name)
            away_team = await _get_or_create_team(db, away_name)

            # Найдём матч по командам и приблизительной дате
            match_date = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
            match = await db.scalar(
                select(Match).where(
                    Match.home_team_id == home_team.id,
                    Match.away_team_id == away_team.id,
                    Match.kickoff >= match_date,
                    Match.kickoff < match_date.replace(hour=23, minute=59),
                )
            )

            if match:
                # Сохраняем xG
                match.home_score = match_data.get("h_goals", 0)
                match.away_score = match_data.get("a_goals", 0)
                # Обновляем статус, если есть счёт
                if match_data.get("h_goals") is not None:
                    match.status = "finished"

                # Добавляем xG в отдельную таблицу или в JSONB поле predictions
                # Пока для простоты сохраним в поле predicted_score как xG
                if not match.predictions:
                    match.home_xg = match_data.get("h_xg", 0)
                    match.away_xg = match_data.get("a_xg", 0)
                await db.commit()
                logger.info(f"Обновлён xG для {home_name} vs {away_name}")

    logger.info(f"Сбор xG из Understat для лиги {league_name} завершён.")


async def _get_or_create_team(db: AsyncSession, name: str) -> Team:
    result = await db.execute(select(Team).where(Team.name == name))
    team = result.scalar_one_or_none()
    if not team:
        team = Team(id=uuid.uuid4(), name=name)
        db.add(team)
        await db.flush()
    return team
