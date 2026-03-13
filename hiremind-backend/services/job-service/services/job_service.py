from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from models.job_post import JobPost
from schemas.job_post import JobPostCreateSchema


def _serialize_job(job: JobPost) -> dict:
    return {
        "id": str(job.id),
        "title": job.title,
        "description": job.description,
        "skills": job.skills,
        "experience": job.experience,
        "location": job.location,
        "ctc": job.ctc,
        "start_time": job.start_time.isoformat(),
        "end_time": job.end_time.isoformat(),
        "created_by": job.created_by,
        "created_at": job.created_at.isoformat(),
    }


async def _get_or_404(job_id: str) -> JobPost:
    try:
        obj_id = PydanticObjectId(job_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format",
        )
    job = await JobPost.get(obj_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


async def create_job(data: JobPostCreateSchema, created_by: str) -> dict:
    job = JobPost(
        title=data.title,
        description=data.description,
        skills=data.skills,
        experience=data.experience,
        location=data.location,
        ctc=data.ctc,
        start_time=data.start_time,
        end_time=data.end_time,
        created_by=created_by,
    )
    await job.insert()
    return _serialize_job(job)


async def get_all_jobs() -> list:
    jobs = await JobPost.find_all().sort(-JobPost.created_at).to_list()
    return [_serialize_job(job) for job in jobs]


async def get_job_by_id(job_id: str) -> dict:
    job = await _get_or_404(job_id)
    return _serialize_job(job)


async def delete_job(job_id: str, user_id: str) -> dict:
    job = await _get_or_404(job_id)
    if job.created_by != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this job",
        )
    await job.delete()
    return {"message": "Job deleted successfully", "job_id": job_id}



async def get_all_jobs() -> list:
    jobs = await Job.find().sort(-Job.created_at).to_list()
    return [_serialize_job(job) for job in jobs]


async def get_job_by_id(job_id: str) -> dict:
    try:
        job = await Job.get(job_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format",
        )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return _serialize_job(job)


async def delete_job(job_id: str, user_id: str) -> dict:
    try:
        job = await Job.get(job_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format",
        )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    if job.created_by != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this job",
        )
    await job.delete()
    return {"message": "Job deleted successfully", "job_id": job_id}
