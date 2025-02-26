from sqlmodel import SQLModel
from app.database.models.hr_models import engine
from app.services.data_ingestion_service import (
    insert_isochrone_data,
    insert_zams_data,
    insert_star_clusters
)

def init_db():
    SQLModel.metadata.create_all(engine)
    print("Inserting initial data...")
    insert_isochrone_data()
    insert_zams_data()
    insert_star_clusters()
    print("Database populated successfully.")
    
if __name__ == '__main__':
    init_db()