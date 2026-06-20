from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from prometheus_fastapi_instrumentator import Instrumentator   # временно отключено
from app.api.v1 import auth, users, predictions, matches, analytics, payments, referrals
from app.core.config import settings
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="SoccerMind AI",
    description="AI-powered football predictions platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentator().instrument(app).expose(app)   # временно отключено

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["predictions"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["matches"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(referrals.router, prefix="/api/v1/referrals", tags=["referrals"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}