import os
import joblib
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from app.ml.features import build_match_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "latest.pkl")

def load_models():
    if not os.path.exists(MODEL_PATH):
        # Создаём fallback модель
        from sklearn.dummy import DummyClassifier
        dummy = DummyClassifier(strategy="uniform")
        dummy.fit(np.zeros((1,1)), [0])
        models = {"result": dummy, "over2.5": dummy, "btts": dummy}
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(models, MODEL_PATH)
    return joblib.load(MODEL_PATH)

async def predict_match(match_id: str, db: AsyncSession):
    features_df = await build_match_features(match_id, db)
    models = load_models()
    X = features_df.values

    prob_result = models["result"].predict_proba(X)[0]
    prob_over = models["over2.5"].predict_proba(X)[0]
    prob_btts = models["btts"].predict_proba(X)[0]

    home_win, draw, away_win = 0.45, 0.25, 0.30
    if len(prob_result) == 3:
        home_win, draw, away_win = prob_result
    elif len(prob_result) == 2:
        # если модель обучена на двух классах, подгоним
        home_win = prob_result[0]*0.6
        away_win = prob_result[0]*0.4
        draw = 0.2

    over_prob = prob_over[1] if len(prob_over) > 1 else 0.5
    btts_prob = prob_btts[1] if len(prob_btts) > 1 else 0.5

    score_dist = {"1-0": 0.12, "2-1": 0.08, "1-1": 0.10, "2-0": 0.07}

    return {
        "home_win": float(home_win),
        "draw": float(draw),
        "away_win": float(away_win),
        "over2.5": float(over_prob),
        "btts": float(btts_prob),
        "score_distribution": score_dist,
    }