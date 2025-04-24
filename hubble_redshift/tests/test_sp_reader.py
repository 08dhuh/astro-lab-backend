import os
import pandas as pd
from galaxy_spectra.sp_reader import read_fallback_spectra
from galaxy_spectra.config import FALLBACK_SP_DIR, GL_IDENTIFIERS

def test_read_fallback_spectra_real_files():
    spectra = read_fallback_spectra()
    print(spectra)
