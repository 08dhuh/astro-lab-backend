from fastapi import APIRouter
from app.services.db_service import check_database_status

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to Astro Lab Backend!"}


@router.get("/db-status")
def db_status():
    return check_database_status()