from sqlmodel import SQLModel
from app.database.models.hr_models import engine

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()