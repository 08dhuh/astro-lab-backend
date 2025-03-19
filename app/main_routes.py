from fastapi import APIRouter
from app.api.routes.db_routes import router as db_router

router = APIRouter()
@router.get("/")
async def root():
    return {"message": "Welcome to Astro Lab Backend!"}

router.include_router(db_router, prefix="/api", tags=['database'])
