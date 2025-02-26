from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
import os

#TODO: .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DATABASE_PATH = os.path.join(BASE_DIR, "..", "..", "database.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
# DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

#print(f"DEBUG: Using database at {DATABASE_URL}")  #TODO: centralised logging

class StarCluster(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    star_count: int
    reddening: Optional[float] = None #E(B-V)
    fe_h: Optional[float] = None #[Fe/H]
    distance_pc: Optional[float] = None #distance in parsecs
    log_age: Optional[float] = None #log age in years

class ClusterUBV(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cluster_id: int = Field(foreign_key="starcluster.id")
    v_mag: float #Apparent V-band magnitude
    b_v: float  #B-V colour index


class ZAMS(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    b_v: float
    Mv: float

class Isochrone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Z: float
    log_age: float
    Mv: float
    b_v:float
    #extra_columns: Optional[str] = None #JSON-encoded, optional columns

