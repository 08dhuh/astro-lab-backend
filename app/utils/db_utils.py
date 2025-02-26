from sqlmodel import Session, select
from sqlalchemy.sql import text
from app.database.models.hr_models import Isochrone, ZAMS, StarCluster, engine


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

def is_database_ready():
    """Check if tables exist and have data."""
    with Session(engine) as session:
        has_isochrones = session.exec(select(Isochrone)).first() is not None
        has_zams = session.exec(select(ZAMS)).first() is not None
        has_clusters = session.exec(select(StarCluster)).first() is not None

        return has_isochrones and has_zams and has_clusters