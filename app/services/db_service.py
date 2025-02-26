from sqlmodel import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.hr_models import engine

from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.hr_models import StarCluster, ZAMS, Isochrone, engine

def get_table_contents(model):
    """Returns a table."""
    try:
        with Session(engine) as session:
            count = session.exec(select(model)).count()
            if count == 0:
                return {"status": "empty", "message": f"{model.__tablename__} has no records."}

            sample_data = session.exec(select(model)).all()

            return {
                "status": "ok",
                "record_count": count,
                "sample_data": [row.dict() for row in sample_data]
            }

    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected failure: {str(e)}"}


def check_database_status():
    """Returns a list of tables in the database."""
    try:
        with Session(engine) as session:
            query = text("SELECT name FROM sqlite_master WHERE type='table';")
            tables = session.exec(query).all()
            if not tables:
                return {"error": "No tables found, database may be empty or corrupted"}
            
            print(f"Retrieved tables -> {tables}") #TODO: logging - DEBUG

            table_list = [t[0] for t in tables if t] 

            if not table_list:
                return {"error": "No tables found"}
            return {"tables": table_list}

    except SQLAlchemyError as e:
        print(f"error: {e}")
        return {"error":f"Database connection error{str(e)}"}
    except Exception as e:
        print(f"error: {e}")
        return {"error": f"Unexpected error occurred, {e}"}

