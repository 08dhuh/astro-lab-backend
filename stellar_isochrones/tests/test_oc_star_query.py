import pytest
from stellar_isochrones.open_cluster_individual_query_process import query_cluster_ubv

def test_query_cluster_bv_obs():
    #random cluster
    cluster_id = 'mel022'
    hr_df = query_cluster_ubv(cluster_id)
    assert not hr_df.empty
    #print(hr_df)

if __name__ == "__main__":
    pytest.main()