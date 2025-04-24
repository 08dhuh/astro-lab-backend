import pandas as pd
import numpy as np
from astroquery.simbad import Simbad
#from galaxy_spectra.config import SIMBAD_FIELDS, COLNAMES

Simbad.add_votable_fields("z_value", "rv_value", "flux(B)", "ids")

def fetch_galaxy_metadata(
    galaxy_identifiers: list[str],
    colnames=('id', 'ra', 'dec', 'z', 'rv', 'flux_b', 'aliases')
) -> pd.DataFrame:
    records = []

    for gid in galaxy_identifiers:
        try:
            result = Simbad.query_object(gid)
            if result is not None:
                record = {
                    "id": gid,
                    "ra": str(result["RA"][0]),
                    "dec": str(result["DEC"][0]),
                    "z": float(result["Z_VALUE"][0]) if result["Z_VALUE"][0] is not np.ma.masked else None,
                    "rv": float(result["RV_VALUE"][0]) if result["RV_VALUE"][0] is not np.ma.masked else None,
                    "flux_b": float(result["FLUX_B"][0]) if result["FLUX_B"][0] is not np.ma.masked else None,
                    "aliases": str(result["IDS"][0]).replace("|", ", ").strip()
                }
                records.append({k: record[k] for k in colnames})
            else:
                print(f"No result for {gid}")
        except Exception as e:
            print(f"{gid}: {e}")
    
    return pd.DataFrame(records)