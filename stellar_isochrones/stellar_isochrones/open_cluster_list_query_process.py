import requests
from bs4 import BeautifulSoup
import pandas as pd
from astroquery.vizier import Vizier
from stellar_isochrones.config import OC_LIST_URL, LYNGA_CAT_BASE_URL, VIZIER_CLUSTER_CATALOGUE, VIZIER_QUERY_COLUMNS

# class StarCluster(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     star_count: int
#     reddening: Optional[float] = None #E(B-V)
#     fe_h: Optional[float] = None #[Fe/H]
#     distance_pc: Optional[float] = None #distance in parsecs
#     log_age: Optional[float] = None #log age in years

# class ClusterUBV(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     cluster_id: int = Field(foreign_key="starcluster.id")
#     v_mag: float #Apparent V-band magnitude
#     b_v: float  #B-V colour index

cluster_df_columns = ['id', 'name', 'star_count']


def request_cluster_list_raw(oc_list_url: str) -> list[str]:
    response = requests.get(oc_list_url)
    bs = BeautifulSoup(response.text, "html.parser")
    anchors = bs.find_all("a")  # cluster id, infos are stored in 'anchor' tags
    anchors.pop()  # to ensure an even number of items
    return anchors


def extract_cluster_info(a1, a2) -> tuple:  #
    """helper function
    accepts a1, a2; a pair of consecutive anchor items of the same cluster from the list"""
    cluster_id = a1['href'].split('=')[1]
    cluster_name = a1.text.strip()
    cluster_star_count = int(a2.text.strip())
    return (cluster_id, cluster_name, cluster_star_count)


def store_cluster_info(anchors: list) -> list:
    """accepts the list of anchors returned from calling the {methodname placeholder} method"""
    num_individual_cluster = len(anchors)//2
    cluster_info_list = []
    for i in range(num_individual_cluster):
        cluster_info_list.append(extract_cluster_info(
            anchors[2 * i], anchors[2 * i + 1]))
    return cluster_info_list


def store_cluster_info_to_pandas(anchors: list) -> pd.DataFrame:
    cluster_info_list = store_cluster_info(anchors)
    cluster_df = pd.DataFrame(cluster_info_list, columns=cluster_df_columns or [
                              'id', 'name', 'star_count'])
    return cluster_df


def query_vizier_catalogue(catalogue=VIZIER_CLUSTER_CATALOGUE,
                           columns=VIZIER_QUERY_COLUMNS) -> pd.DataFrame:
    cat = Vizier(columns=columns,
                 row_limit=-1  # limitless
                 ).get_catalogs(catalogue)[0]
    cat = cat.to_pandas()
    cat.columns = columns
    cat.sort_values(by='Cluster', na_position='first').reset_index(drop=True)
    return cat



def merge_clusters(cluster_df: pd.DataFrame,
                   cat_df: pd.DataFrame) -> pd.DataFrame:
    merged_cluster_df = pd.merge(
        cluster_df,
        cat_df,
        left_on='name',
        right_on='Cluster',
        how='left'
    )
    merged_cluster_df.drop(columns='Cluster', inplace=True)
    return merged_cluster_df

def find_missing_reddening_rows(merged_cluster_df: pd.DataFrame):
    return merged_cluster_df[merged_cluster_df['E(B-V)'].isna()].reset_index(drop=True)

    # common_clusters = names1 & names2
    # missing_clusters = names1 - common_clusters

def lynga_url(dirname): return LYNGA_CAT_BASE_URL.format(dirname=dirname)


def extract_data_from_pre(html_content:str) -> dict:
    """
    Extracts E(B-V) and log(age) values from a <pre> block in the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    pre = soup.find('pre')

    if pre is None:
        return {}

    pre_text = pre.get_text()
    lines = pre_text.splitlines()

    extracted_data = {}

    for line in lines:
        if 'E(B-V)' in line:
            try:
                value = float(line.split()[-1]) # Try to convert to float, store only if successful
                extracted_data['E(B-V)'] = value
            except (ValueError, IndexError): #skip this line                 
                pass
        elif 'Derived log(age)' in line:
            try:         
                value = float(line.split()[-1])
                extracted_data['Derived log(age)'] = value
            except (ValueError, IndexError):
                pass

    return extracted_data



def fill_missing_reddening_values(merged_df:pd.DataFrame) -> pd.DataFrame:
    reddening_missing_rows = find_missing_reddening_rows(merged_cluster_df=merged_df)
    for _, missing_row in reddening_missing_rows.iterrows():
        row_id = missing_row['id']    
        lynga_query_url = lynga_url(row_id)    
        result = requests.get(lynga_query_url).text
    
        extracted_data = extract_data_from_pre(result)

        if 'E(B-V)' in extracted_data: #updates the missing values
            ebv_value = extracted_data['E(B-V)']
            merged_df.loc[merged_df['id'] == row_id, 'E(B-V)'] = ebv_value
    
        if 'Derived log(age)' in extracted_data:
            age_value = extracted_data['Derived log(age)']
            merged_df.loc[merged_df['id'] == row_id, 'Age'] = age_value
    return merged_df

def query_open_cluster_table(): # method encapsulating the cluster query logics
    anchors = request_cluster_list_raw(OC_LIST_URL)
    cluster_list_df = store_cluster_info_to_pandas(anchors)
    cat_df = query_vizier_catalogue()
    merged_df = merge_clusters(cluster_list_df, cat_df)
    return fill_missing_reddening_values(merged_df)