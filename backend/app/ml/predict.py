import os
import joblib
import pandas as pd
import numpy as np
from scipy.stats import poisson
from sqlalchemy.ext.asyncio import AsyncSession
from app.ml.features import build_match_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "latest.pkl")

def load_models():
    if not os.path.exists(MODEL_PATH):
        from sklearn.dummy import DummyClassifier
        dummy = DummyClassifier(strategy="uniform")
        dummy.fit(np.zeros((1,1)), [0])
        models = {"result": dummy, "over2.5": dummy, "btts": dummy, "feature_columns": []}
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(models, MODEL_PATH)
    return joblib.load(MODEL_PATH)

def _expected_goals(features_df):
    """Грубая оценка ожидаемых голов на основе средней результативности."""
    home_avg = features_df["home_avg_goals_last5"].values[0]
    away_avg = features_df["away_avg_goals_last5"].values[0]
    home_def = features_df["away_avg_conceded_last5"].values[0]
    away_def = features_df["home_avg_conceded_last5"].values[0]
    # Ожидаемые голы хозяев = (своя атака / защита гостей) * среднее по лиге (1.4)
    home_xg = (home_avg / max(away_def, 0.1)) * 0.7
    away_xg = (away_avg / max(home_def, 0.1)) * 0.7
    return home_xg, away_xg

def _score_probabilities(home_xg, away_xg, max_goals=5):
    """Возвращает словарь {счёт: вероятность} на основе Пуассона."""
    scores = {}
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
            scores[f"{i}-{j}"] = prob
    # Нормализация (сумма по всем сгенерированным счетам < 1, но для простоты оставим как есть, можно отмасштабировать)
    total = sum(scores.values())
    if total > 0:
        scores = {k: v / total for k, v in scores.items()}
    return scores

async def predict_match(match_id: str, db: AsyncSession):
    features_df = await build_match_features(match_id, db)
    models = load_models()

    feature_cols = models.get("feature_columns", [])
    if feature_cols:
        X = features_df[feature_cols].values
    else:
        X = features_df.values

    prob_result = models["result"].predict_proba(X)[0]
    prob_over = models["over2.5"].predict_proba(X)[0]
    prob_btts = models["btts"].predict_proba(X)[0]

    home_win = prob_result[0] if len(prob_result) > 0 else 0.45
    draw = prob_result[1] if len(prob_result) > 1 else 0.25
    away_win = prob_result[2] if len(prob_result) > 2 else 0.30

    over_prob = prob_over[1] if len(prob_over) > 1 else 0.5
    btts_prob = prob_btts[1] if len(prob_btts) > 1 else 0.5

    # Точный счёт через Пуассона
    home_xg, away_xg = _expected_goals(features_df)
    score_dist = _score_probabilities(home_xg, away_xg)

    return {
        "home_win": float(home_win),
        "draw": float(draw),
        "away_win": float(away_win),
        "over2.5": float(over_prob),
        "btts": float(btts_prob),
        "score_distribution": score_dist,
    }
