import pytest
import pandas as pd
import os
from stellar_isochrones.isochrones_loader import load_isochrones_from_files
from stellar_isochrones.config import ISOCHRONE_COLUMNS
def test_load_isochrones_from_files():
    df = load_isochrones_from_files()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ISOCHRONE_COLUMNS
    assert df["Z"].notna().all()
    assert df["age"].notna().all()
    assert df["Mv"].notna().all()
    assert df["Mb"].notna().all()

    print(df.head(10)) 
    print(df.describe()) 

if __name__ == "__main__":
    pytest.main()
