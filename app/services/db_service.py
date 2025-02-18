from sqlmodel import Session
from sqlalchemy.sql import text
from app.database.models.hr_models import engine

def check_database_status():
    """Returns a list of tables in the database."""
    try:
        with Session(engine) as session:
            query = text("SELECT name FROM sqlite_master WHERE type='table';")
            tables = session.exec(query).all()

            print(f"Retrieved tables -> {tables}") #TODO: logging - DEBUG

            table_list = [t[0] for t in tables]  

            if not table_list:
                return {"error": "No tables found"}
            return {"tables": table_list}

    except Exception as e:
        print(f"error: {e}")
        return {"error": f"Database connection failed, {e}"}

