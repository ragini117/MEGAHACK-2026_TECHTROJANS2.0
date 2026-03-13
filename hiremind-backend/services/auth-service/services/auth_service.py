from datetime import datetime, timedelta

from beanie import PydanticObjectId
from fastapi import HTTPException
from jose import jwt
import os
from dotenv import load_dotenv

from models.user import User
from models.organization import Organization
from schemas.user import UserRegisterSchema, UserLoginSchema
from utils.password import hash_password, verify_password
from shared.response import success
from shared.status_codes import HTTP

load_dotenv()

JWT_SECRET: str = os.getenv("JWT_SECRET", "change-this-secret-in-production")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def _create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def _serialize_user(user: User) -> dict:
    """Serialize user; performs $lookup for organization if org_id present."""
    org_data = None
    if user.organization_id:
        try:
            org = await Organization.get(PydanticObjectId(user.organization_id))
            if org:
                org_data = {
                    "id": str(org.id),
                    "name": org.name,
                    "industry": org.industry,
                    "size": org.size,
                    "location": org.location,
                }
        except Exception:
            pass

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "phone_no": user.phone_no,
        "organization_id": user.organization_id,
        "organization": org_data,
        "skills": user.skills,
        "experience": user.experience,
        "created_at": user.created_at.isoformat(),
    }


async def register_user(data: UserRegisterSchema):
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(
            status_code=HTTP.CONFLICT,
            detail="An account with this email already exists",
        )

    # ── Step 1: Create Organization first (HR only) ───────────────────────────
    organization_id: str | None = None
    if data.role.value == "hr" and data.organization:
        org = Organization(
            name=data.organization.name,
            industry=data.organization.industry,
            size=data.organization.size,
            location=data.organization.location,
        )
        await org.insert()
        organization_id = str(org.id)

    # ── Step 2: Create User with org reference ────────────────────────────────
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=str(data.role.value),
        phone_no=data.phone_no,
        organization_id=organization_id,
        skills=data.skills,
        experience=data.experience,
    )
    await user.insert()

    token = _create_access_token(
        {"sub": str(user.id), "role": user.role, "email": user.email}
    )

    return success(
        data={"access_token": token, "token_type": "bearer", "user": await _serialize_user(user)},
        message="Account created successfully",
        code=HTTP.CREATED,
    )


async def login_user(data: UserLoginSchema):
    user = await User.find_one(User.email == data.email)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=HTTP.UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = _create_access_token(
        {"sub": str(user.id), "role": user.role, "email": user.email}
    )

    return success(
        data={"access_token": token, "token_type": "bearer", "user": await _serialize_user(user)},
        message="Login successful",
        code=HTTP.OK,
    )


async def get_current_user_info(user_id: str):
    try:
        user = await User.get(PydanticObjectId(user_id))
    except Exception:
        raise HTTPException(
            status_code=HTTP.BAD_REQUEST,
            detail="Invalid user ID",
        )
    if not user:
        raise HTTPException(
            status_code=HTTP.NOT_FOUND,
            detail="User not found",
        )
    return success(data=await _serialize_user(user), message="User fetched successfully")


