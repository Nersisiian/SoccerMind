import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from app.db.models.referral import Referral
from app.db.models.subscription import Subscription
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from jose import jwt
from app.core.config import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_in: UserCreate) -> User:
        existing = await self.db.execute(select(User).where(User.email == user_in.email))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            referral_code=str(uuid.uuid4())[:8],
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        if user_in.referral_code:
            referrer = await self.db.execute(select(User).where(User.referral_code == user_in.referral_code))
            referrer = referrer.scalar_one_or_none()
            if referrer and referrer.id != user.id:
                referral = Referral(referrer_id=referrer.id, referred_id=user.id)
                self.db.add(referral)
                await self.db.commit()

        return user

    async def authenticate_user(self, email: str, password: str):
        user = await self.db.execute(select(User).where(User.email == email))
        user = user.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def refresh_access_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        access_token = create_access_token(data={"sub": user_id})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def get_user_by_id(self, user_id: str) -> User:
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(self, user_id: str, update: UserUpdate) -> User:
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if update.email is not None:
            user.email = update.email
        if update.is_active is not None:
            user.is_active = update.is_active
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_referral_stats(self, user: User):
        refs = await self.db.execute(
            select(Referral).where(Referral.referrer_id == user.id)
        )
        refs = refs.scalars().all()
        return {"referrals_count": len(refs), "earned_credits": len(refs) * 10}