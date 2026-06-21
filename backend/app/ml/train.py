import os
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sqlalchemy.ext.asyncio import AsyncSession
from app.ml.features import build_training_dataset
import logging

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "latest.pkl")

async def train_models(db: AsyncSession):
    logger.info("Начало обучения моделей...")
    try:
        df = await build_training_dataset(db)
    except ValueError as e:
        logger.warning(f"Нет данных для обучения: {e}")
        return

    feature_cols = [c for c in df.columns if c not in ("match_id", "home_win", "draw", "away_win", "total_goals", "btts")]
    X = df[feature_cols]

    # Целевые переменные
    y_result = df[["home_win", "draw", "away_win"]].idxmax(axis=1).map({"home_win": 0, "draw": 1, "away_win": 2})
    y_over = (df["total_goals"] > 2.5).astype(int)
    y_btts = df["btts"]

    model_result = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, use_label_encoder=False, eval_metric='mlogloss', verbosity=0)
    model_over = LGBMClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, verbose=-1)
    model_btts = CatBoostClassifier(iterations=100, depth=5, learning_rate=0.1, verbose=0)

    model_result.fit(X, y_result)
    model_over.fit(X, y_over)
    model_btts.fit(X, y_btts)

    models = {
        "result": model_result,
        "over2.5": model_over,
        "btts": model_btts,
        "feature_columns": feature_cols,
    }

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(models, MODEL_PATH)
    logger.info(f"Модели сохранены в {MODEL_PATH}")
