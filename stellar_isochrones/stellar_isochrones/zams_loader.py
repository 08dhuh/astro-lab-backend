import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from stellar_isochrones.config import ZAMS_FILE

def read_zams(filepath:str=ZAMS_FILE) -> pd.DataFrame:
    return pd.read_csv(filepath, usecols=['b_v', 'Mv'])

def interpolate_zams(zams_df_raw: pd.DataFrame, 
                     num_points=500) -> pd.DataFrame:
    b_v_raw, mv_raw = zams_df_raw['b_v'], zams_df_raw['Mv']
    b_v_values = np.linspace(min(b_v_raw), max(b_v_raw), num_points) #b_v raw has monotonically increasing values
    cs = CubicSpline(b_v_raw, mv_raw)
    m_v_values = cs(b_v_values)
    return pd.DataFrame({'b_v': b_v_values, 'Mv': m_v_values})

def load_interpolated_zams(interpolate:bool=True, 
                           num_points=500) -> pd.DataFrame:
    """Wrapper function that reads and interpolates ZAMS in one step."""
    raw_zams = read_zams()
    if interpolate:
        return interpolate_zams(raw_zams, num_points)
    return raw_zams