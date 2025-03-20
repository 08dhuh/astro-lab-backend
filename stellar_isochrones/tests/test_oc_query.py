import pytest
from stellar_isochrones.open_cluster_list_query_process import *
from stellar_isochrones.config import OC_LIST_URL, OC_UVB_BASE_URL, LYNGA_CAT_BASE_URL
# def test_usage():
#     anchors = request_cluster_list_raw(OC_LIST_URL)
#     cluster_list_df = store_cluster_info_to_pandas(anchors)

# def test_vizier_query():
#     cat = query_vizier_catalogue()
#     print(cat.describe())


def test_query_open_cluster_table():
    pass
    #df = query_open_cluster_table()
    #print(df.describe())
    #print(df.head(10))

if __name__ == "__main__":
    pytest.main()
