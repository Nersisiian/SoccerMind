from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserOut, Token
from app.services.auth_service import AuthService
from app.core.rate_limit import limiter
from slowapi.util import get_remote_address
from app.db.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
@limiter.limit("5/minute")
async def register(request: Request, user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).register_user(user_in)

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await AuthService(db).authenticate_user(form_data.username, form_data.password)

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).refresh_access_token(refresh_token)

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
