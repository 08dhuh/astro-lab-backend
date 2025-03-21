from fastapi import FastAPI
from sqlmodel import Session, select
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.hr_models import StarCluster, ZAMS, ClusterUBV, Isochrone, engine


# TODO: centralised logging


def query_isochrone(log_age: float, Z: float, app: FastAPI):
    isochrone_data = getattr(app.state, "isochrone_data", None)
    if isochrone_data is None:
        return {"error": "Isochrone data not loaded"}

    filtered = isochrone_data[
        (isochrone_data["log_age"] == log_age) & (isochrone_data["Z"] == Z)
    ]
    print(filtered)

    return {
        "log_age": float(log_age),
        "Z": float(Z),
        #"data": filtered[["b_v", "Mv"]].tolist()
        "data": [{"b_v": float(row[2]), "Mv": float(row[3])} for row in filtered]


    }


def get_all_clusters():
    """Returns all open cluster info."""
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


def get_isochrones(limit: int = 1000):  # pagination needed?
    try:
        with Session(engine) as session:
            return session.exec(select(Isochrone).limit(limit)).all()
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}


def get_cluster_ubv(cluster_pk: int):
    try:
        with Session(engine) as session:
            return session.exec(select(ClusterUBV).where(ClusterUBV.cluster_pk == cluster_pk)).all()
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected failure: {str(e)}"}


def find_missing_cluster_pks():
    with Session(engine) as session:
        existing_pks = sorted(set(session.exec(select(ClusterUBV.cluster_pk))))

        if not existing_pks:
            print("No cluster UBV data found.")
            return []

        expected_pks = set(range(min(existing_pks), max(existing_pks) + 1))
        missing_pks = sorted(expected_pks - set(existing_pks))

        return missing_pks


def check_database_status():
    """Returns a list of tables in the database."""
    try:
        with Session(engine) as session:
            query = text("SELECT name FROM sqlite_master WHERE type='table';")
            tables = session.exec(query).all()
            if not tables:
                return {"error": "No tables found, database may be empty or corrupted"}

            print(f"Retrieved tables -> {tables}")  # TODO: logging - DEBUG

            table_list = [t[0] for t in tables if t]

            if not table_list:
                return {"error": "No tables found"}
            return {"tables": table_list}

    except SQLAlchemyError as e:
        print(f"error: {e}")
        return {"error": f"Database connection error{str(e)}"}
    except Exception as e:
        print(f"error: {e}")
        return {"error": f"Unexpected error occurred, {e}"}
