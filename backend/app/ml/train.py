import os
import joblib
import pandas as pd
import numpy as np
from optuna import create_study
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sqlalchemy.ext.asyncio import AsyncSession

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "latest.pkl")

def train_xgboost(X, y):
    model = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss')
    model.fit(X, y)
    return model

def train_lightgbm(X, y):
    model = LGBMClassifier(n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X, y)
    return model

def train_catboost(X, y):
    model = CatBoostClassifier(iterations=100, depth=5, learning_rate=0.1, verbose=0)
    model.fit(X, y)
    return model

async def train_models(db: AsyncSession):
    # Загрузка исторических данных из БД
    query = "SELECT ... FROM matches JOIN ..."  # упрощено: создадим синтетику
    # Для демонстрации генерируем случайные данные
    np.random.seed(42)
    X = pd.DataFrame(np.random.randn(1000, 10), columns=[f"feat_{i}" for i in range(10)])
    y_result = np.random.choice([0,1,2], 1000)  # 0-home,1-draw,2-away
    y_over = np.random.choice([0,1], 1000)
    y_btts = np.random.choice([0,1], 1000)

    model_result = train_xgboost(X, y_result)
    model_over = train_lightgbm(X, y_over)
    model_btts = train_catboost(X, y_btts)

    models = {
        "result": model_result,
        "over2.5": model_over,
        "btts": model_btts,
    }

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(models, MODEL_PATH)
    print(f"Models saved to {MODEL_PATH}")