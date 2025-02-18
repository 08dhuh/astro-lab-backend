from sqlmodel import Session
from sqlalchemy.sql import text
from app.database.models.hr_models import engine

def get_existing_tables():
    """Returns a list of tables in the database."""
    with Session(engine) as session:
        query = text("SELECT name FROM sqlite_master WHERE type='table';")
        tables = session.exec(query).all()
        return tables

if __name__ == "__main__":
    tables = get_existing_tables()
    if tables:
        print(f"Tables: {tables}")
    else:
        print("No tables found. Run `python -m app.database.init_db` to initialise.")
