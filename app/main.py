from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.utils.db_utils import is_database_ready


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not is_database_ready():
        print("Database is not ready. Run `python app/database/init_db.py` to populate it.")
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(router)
