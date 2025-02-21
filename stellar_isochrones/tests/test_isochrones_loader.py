import pytest
import pandas as pd
#import os
from stellar_isochrones.isochrones_loader import *
from stellar_isochrones.config import ISOCHRONE_COLUMNS

def test_load_isochrones_from_files():
    df = load_isochrones_from_default_files()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ISOCHRONE_COLUMNS
    assert df["Z"].notna().all()
    assert df["age"].notna().all()
    assert df["Mv"].notna().all()
    assert df["Mb"].notna().all()

    #print(df.head(10)) 
    #print(df.describe()) 

def test_read_default_isochrones():
    try:
        df = read_default_isochrones()
        print(df.head(10))
        print(df.describe())
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert list(df.columns) == ISOCHRONE_SCHEMA_LIST

        assert df['Z'].dtype == float
        assert df['log_age'].dtype == float
        assert df['Mv'].dtype == float
        assert df['b_v'].dtype == float

        assert not df.isnull().any().any()

        assert df['Z'].min() > 0
        assert 7.8 <= df['log_age'].min() <= 10.25
    except Exception as e:
        pytest.fail(f'Test failed for the following reason: {e}')


if __name__ == "__main__":
    pytest.main()
