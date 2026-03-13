"""
Shared FastAPI auth dependencies — import into any route file.

Provides:
    get_current_user    — validates Bearer token, returns payload dict
    require_hr          — only allows users with role "hr"
    require_candidate   — only allows users with role "candidate"
    get_optional_user   — returns payload if token present, else None

Usage:
    from shared.dependencies import get_current_user, require_hr, require_candidate

    @router.get("/jobs")
    async def list_jobs(current_user: dict = Depends(get_current_user)):
        user_id = current_user["sub"]
        role    = current_user["role"]
        email   = current_user["email"]

    @router.post("/jobs")
    async def create_job(current_user: dict = Depends(require_hr)):
        ...

    @router.post("/apply")
    async def apply(current_user: dict = Depends(require_candidate)):
        ...
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.jwt_handler import decode_access_token
from shared.status_codes import HTTP

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Validate Bearer token and return the decoded payload.

    Payload keys:
        sub   — user ID (str)
        role  — "hr" or "candidate"
        email — user email
        exp   — expiry timestamp
    """
    return decode_access_token(credentials.credentials)


async def require_hr(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Allow only users with role 'hr'. Raises 403 otherwise."""
    if current_user.get("role") != "hr":
        raise HTTPException(
            status_code=HTTP.FORBIDDEN,
            detail="Access denied — HR role required",
        )
    return current_user


async def require_candidate(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Allow only users with role 'candidate'. Raises 403 otherwise."""
    if current_user.get("role") != "candidate":
        raise HTTPException(
            status_code=HTTP.FORBIDDEN,
            detail="Access denied — candidate role required",
        )
    return current_user


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_optional),
) -> dict | None:
    """
    Return decoded token payload if a valid Bearer token is present,
    otherwise return None (no error). Useful for public routes that
    optionally enrich the response when a user is logged in.
    """
    if not credentials:
        return None
    try:
        return decode_access_token(credentials.credentials)
    except HTTPException:
        return None
