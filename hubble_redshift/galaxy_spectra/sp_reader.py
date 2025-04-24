
import pandas as pd
import os
# from astroquery.sdss import SDSS
# from astropy import coordinates as coords
# import astropy.units as u

import glob
from galaxy_spectra.config import FALLBACK_SP_DIR, FALLBACK_SP_GLOB_PATTERN, GL_IDENTIFIERS


def read_fallback_spectra():
    spectra = {}
    available_files = glob.glob(FALLBACK_SP_GLOB_PATTERN)
    for file_path in available_files:
        filename = os.path.basename(file_path)
        name = filename.replace(".SP", "")

        if name in [gid.replace(" ", "") for gid in GL_IDENTIFIERS]:
            try:
                df = pd.read_csv(file_path, sep='\\s+', names=["wavelength", "intensity"])
                spectra[name] = df
            except Exception as e:
                print(f"[ERROR] Could not read {filename}: {e}")

    return spectra