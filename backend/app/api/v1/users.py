from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserOut, UserUpdate
from app.services.auth_service import AuthService
from app.core.permissions import RoleChecker

router = APIRouter()
admin_only = RoleChecker(["admin"])

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin" and str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await AuthService(db).get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, update: UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if str(current_user.id) != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    return await AuthService(db).update_user(user_id, update)