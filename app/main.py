#import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
#from dotenv import load_dotenv
from app.main_routes import router
from app.utils.db_utils import is_database_ready



@asynccontextmanager
async def lifespan(app: FastAPI):
    if not is_database_ready():
        print("Database is not ready. Run `python app/database/init_db.py` to populate it.")
    yield

app = FastAPI(lifespan=lifespan)

# load_dotenv()
# origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(router)
