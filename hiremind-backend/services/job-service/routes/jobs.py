from fastapi import APIRouter, Depends, status

from schemas.job_post import JobPostCreateSchema
from services.job_service import create_job, get_all_jobs, get_job_by_id, delete_job
from shared.dependencies import get_current_user, require_hr

router = APIRouter()


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def create_new_job(
    data: JobPostCreateSchema,
    current_user: dict = Depends(require_hr),
):
    return await create_job(data, current_user["sub"])


@router.get("/jobs")
async def list_all_jobs():
    return await get_all_jobs()


@router.get("/jobs/{job_id}")
async def get_single_job(job_id: str):
    return await get_job_by_id(job_id)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_200_OK)
async def remove_job(
    job_id: str,
    current_user: dict = Depends(require_hr),
):
    return await delete_job(job_id, current_user["sub"])
