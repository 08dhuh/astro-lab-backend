import pandas as pd
import glob
from stellar_isochrones.config import ISOCHRONE_FILE_GLOB_PATTERN, ISOCHRONE_COLUMNS, ISOCHRONE_SCHEMA_LIST

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


def load_isochrones_from_default_files(file_path:str = ISOCHRONE_FILE_GLOB_PATTERN,
                               columns:list = ISOCHRONE_COLUMNS,
                               data_column_offset:int = 2,
                               meta_index_offset:int = 2) -> pd.DataFrame:
    """Load isochrone data from default files and return a pandas DataFrame"""
    isochrone_file_paths = glob.glob(file_path)
    # isochrone_columns = ["Z", "age","log_age", "M_ini", "M_act", "logL/Lo", "logTe", "logG",
    #          "Mv", "u_b", "b_v", "v_i", "stage"]
    col_num = len(columns) - data_column_offset 
    meta_index_offset = meta_index_offset

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
    if not isochrone_records:
        raise ValueError("No valid isochrone records found in the specified files.")
    df = pd.DataFrame(isochrone_records, columns=ISOCHRONE_COLUMNS)
    df = df.apply(pd.to_numeric, errors='coerce')
    # for col in df.columns[:-1]:
    #     df[col] = pd.to_numeric(df[col])
    
    return df

def process_default_isochrone_records(df_raw:pd.DataFrame,
                                      #columns:list = ISOCHRONE_COLUMNS,
                                      sql_cols:list = ISOCHRONE_SCHEMA_LIST):
    """Convert raw isochrone data into a DataFrame that adheres to the SQL schema.
    """
    #ISOCHRONE_COLUMNS = [
#     "Z", "age", "log_age", "M_ini", "M_act", "logL/Lo", "logTe", "logG",
#     "Mbol", "Mu", "Mb", "Mv", "Mr", "Mi", "Mj", "Mh", "Mk", "Flum"
# ]
    #ISOCHRONE_SCHEMA_LIST = ['Z','log_age','Mv','b_v']
    try:
        df = df_raw[['Z', 'log_age', 'Mv']].copy()
        df.loc[:, 'b_v'] = df_raw['Mb'] - df_raw['Mv']
        return df[sql_cols]
    except KeyError as e:
        # TODO: logging
        raise KeyError(f"Missing required columns in the dataset: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing isochrone records: {e}")

def read_default_isochrones(file_path:str = ISOCHRONE_FILE_GLOB_PATTERN,
                               columns:list = ISOCHRONE_COLUMNS,
                               data_column_offset:int = 2,
                               meta_index_offset:int = 2,
                               sql_cols:list = ISOCHRONE_SCHEMA_LIST
                               ):
    """Read, process, and return isochrone data as a DataFrame."""
    df_raw = load_isochrones_from_default_files(file_path=file_path,
                                                columns=columns,
                                                data_column_offset=data_column_offset,
                                                meta_index_offset=meta_index_offset)
    return process_default_isochrone_records(df_raw,
                                           sql_cols=sql_cols)

    


def read_isochrones():
    #abstract method to read isochrone data from external resources
    raise NotImplementedError("This method must be implemented for external resource loading.")


