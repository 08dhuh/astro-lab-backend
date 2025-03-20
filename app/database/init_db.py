from sqlmodel import SQLModel
from app.database.models.hr_models import engine
from app.services.data_ingestion_service import (
    insert_isochrone_data,
    insert_zams_data,
    insert_star_clusters,
    insert_cluster_ubv_data
)

def setup_db():
    try:
        SQLModel.metadata.create_all(engine)
        print("Inserting initial data...")
        insert_isochrone_data()
        insert_zams_data()
        insert_star_clusters()
        print("Database populated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def setup_ubv_db():
    try:
        print("Fetching and inserting ubv data for every cluster...")
        insert_cluster_ubv_data()
        print("UBV data population successful.")
    except Exception as e:
        print(f"Error: {e}")
        raise e

if __name__ == '__main__':
    setup_db()
    setup_ubv_db()