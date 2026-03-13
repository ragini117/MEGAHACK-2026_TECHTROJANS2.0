from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from models.organization import Organization
from schemas.organization import (
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
    OrganizationResponseSchema,
)
from shared.response import success
from shared.status_codes import HTTP

router = APIRouter(prefix="/organizations", tags=["Organizations"])


# ── helper ────────────────────────────────────────────────────────────────────

def _serialize(org: Organization) -> dict:
    return {
        "id": str(org.id),
        "name": org.name,
        "industry": org.industry,
        "size": org.size,
        "location": org.location,
        "created_at": org.created_at.isoformat(),
    }


async def _get_or_404(org_id: str) -> Organization:
    try:
        obj_id = PydanticObjectId(org_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP.BAD_REQUEST,
            detail="Invalid organization ID format",
        )
    org = await Organization.get(obj_id)
    if not org:
        raise HTTPException(
            status_code=HTTP.NOT_FOUND,
            detail=f"Organization '{org_id}' not found",
        )
    return org


# ── CREATE ────────────────────────────────────────────────────────────────────

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(payload: OrganizationCreateSchema):
    """Create a new organization."""
    org = Organization(
        name=payload.name,
        industry=payload.industry,
        size=payload.size,
        location=payload.location,
    )
    await org.insert()
    return success(data=_serialize(org), message="Organization created successfully", code=HTTP.CREATED)


# ── READ ALL ──────────────────────────────────────────────────────────────────

@router.get("")
async def get_all_organizations():
    """List all organizations, sorted newest first."""
    orgs = await Organization.find_all().sort(-Organization.created_at).to_list()
    return success(data=[_serialize(o) for o in orgs], message="Organizations fetched successfully")


# ── READ BY ID ────────────────────────────────────────────────────────────────

@router.get("/{org_id}")
async def get_organization(org_id: str):
    """Get a single organization by ID."""
    org = await _get_or_404(org_id)
    return success(data=_serialize(org), message="Organization fetched successfully")


# ── UPDATE ────────────────────────────────────────────────────────────────────

@router.put("/{org_id}")
async def update_organization(org_id: str, payload: OrganizationUpdateSchema):
    """Partially update an organization."""
    org = await _get_or_404(org_id)

    update_data = payload.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=HTTP.BAD_REQUEST, detail="No update fields provided")

    for field, value in update_data.items():
        setattr(org, field, value)

    await org.save()
    return success(data=_serialize(org), message="Organization updated successfully")


# ── DELETE ────────────────────────────────────────────────────────────────────

@router.delete("/{org_id}")
async def delete_organization(org_id: str):
    """Delete an organization by ID."""
    org = await _get_or_404(org_id)
    await org.delete()
    return success(data={"id": org_id}, message="Organization deleted successfully")
