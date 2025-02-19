import pandas as pd
import glob
from stellar_isochrones.config import ISOCHRONE_FILE_GLOB_PATTERN, ISOCHRONE_COLUMNS

#Y = Y_primordial + del_Y/del_Z * Z

#	Isochrone	Z = 0.00100		Age = 	6.310e+07 yr
# log(age/yr)	M_ini   	M_act	logL/Lo	logTe	logG	Mbol 	Mu 	Mb 	Mv 	Mr 	Mi 	Mj 	Mh 	Mk 	Flum
# class Isochrone(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     Z: float
#     log_age: float
#     Mv: float
#     b_v:float
#     extra_columns: Optional[str] = Non

# default file schema conversion table : Z -> Z
# log(age/yr) -> log_age
# Mv ->  Mv
# B-V -> b_v
# ISOCHRONE_COLUMNS = [
#     "Z", "age", "log_age", "M_ini", "M_act", "logL/Lo", "logTe", "logG",
#     "Mbol", "Mu", "Mb", "Mv", "Mr", "Mi", "Mj", "Mh", "Mk", "Flum"
# ]

def load_isochrones_from_files() -> pd.DataFrame:
    """Load isochrone data from default files and return a pandas DataFrame"""
    isochrone_file_paths = glob.glob(ISOCHRONE_FILE_GLOB_PATTERN)
    # isochrone_columns = ["Z", "age","log_age", "M_ini", "M_act", "logL/Lo", "logTe", "logG",
    #          "Mv", "u_b", "b_v", "v_i", "stage"]
    col_num = len(ISOCHRONE_COLUMNS) - 2
    meta_index_offset = 2

    isochrone_records = []
    for fpath in isochrone_file_paths:
        with open(fpath, 'r') as f:
            current_Z = None
            current_age = None

            for line in f:
                line = line.strip()
                if line.startswith('#'):  #metadata line example: #	Isochrone	Z = 0.00100		Age = 	7.079e+07 yr
                    parts = line.split()
                    if 'Z' in parts and 'Age' in parts:
                        current_Z = float(parts[parts.index('Z') + meta_index_offset])
                        current_age = float(parts[parts.index('Age') + meta_index_offset]) #offset by 2 because values appear two positions after labels.
                else:
                    parts = line.split()
                    if len(parts) == col_num:
                        isochrone_records.append([current_Z, current_age] + parts)
    df = pd.DataFrame(isochrone_records, columns=ISOCHRONE_COLUMNS)
    for col in df.columns[:-1]:
        df[col] = pd.to_numeric(df[col])
    
    return df



def read_isochrones():
    #abstract method to read isochrone data from external resources
    pass 


