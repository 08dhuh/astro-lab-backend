import pytest
from stellar_isochrones.zams_loader import load_interpolated_zams
import pandas as pd 
def test_load_interpolated_zams():
    raw_zams = load_interpolated_zams(interpolate=False)
    assert isinstance(raw_zams, pd.DataFrame)
    assert 'b_v' in raw_zams.columns and 'Mv' in raw_zams.columns
    assert len(raw_zams) > 0

    num_points = 500
    interpolated_zams = load_interpolated_zams(interpolate=True, num_points=num_points)
    assert isinstance(interpolated_zams, pd.DataFrame)
    assert len(interpolated_zams) == num_points
    print(f'{__name__} all tests passed')

if __name__ == "__main__":
    pytest.main(["-q", __file__])
    
