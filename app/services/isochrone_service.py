from fastapi import FastAPI
import numpy as np
from sqlmodel import Session, select
from app.database.models.hr_models import Isochrone, engine


def load_isochrones_into_memory(app: FastAPI):
    with Session(engine) as session:
        results = session.exec(select(Isochrone)).all()
    
    isochrone_data = np.array(
        [(row.log_age, row.Z, row.b_v, row.Mv) for row in results], 
        dtype=[("log_age", np.float32), ("Z", np.float32), ("b_v", np.float32), ("Mv", np.float32)]
    )
    app.state.isochrone_data = isochrone_data
    print(f"Loaded {len(isochrone_data)} isochrone entries into memory.")


