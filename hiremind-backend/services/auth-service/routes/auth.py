from fastapi import APIRouter, Depends

from schemas.user import UserRegisterSchema, UserLoginSchema
from services.auth_service import register_user, login_user, get_current_user_info
from shared.dependencies import get_current_user

router = APIRouter()


@router.post("/register")
async def register(data: UserRegisterSchema ):
    return await register_user(data)


@router.post("/login")
async def login(data: UserLoginSchema):
    return await login_user(data)


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return await get_current_user_info(current_user["sub"])
