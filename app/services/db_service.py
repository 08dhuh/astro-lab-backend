from sqlmodel import Session, select
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.hr_models import StarCluster, ZAMS, ClusterUBV, Isochrone, engine

#TODO: centralised logging

def get_all_clusters():
    """Returns all star clusters."""
    try:
        with Session(engine) as session:
            return session.exec(select(StarCluster)).all()

    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected failure: {str(e)}"}
    
def get_all_cluster_UBVS():
    try:
        with Session(engine) as session:
            return session.exec(select(ClusterUBV)).all()
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected failure: {str(e)}"}

def get_isochrones(limit:int = 100):
    try:
        with Session(engine) as session:
            return session.exec(select(Isochrone).limit(limit)).all()
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}

def get_cluster_ubv(cluster_id: int):
    try:
        with Session(engine) as session:
            return session.exec(select(ClusterUBV).where(ClusterUBV.cluster_id == cluster_id)).first()
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

