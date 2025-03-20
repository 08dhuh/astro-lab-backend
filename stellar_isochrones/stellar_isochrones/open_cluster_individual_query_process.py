import io
import requests
from bs4 import BeautifulSoup
import pandas as pd

from stellar_isochrones.config import OC_UVB_BASE_URL, OC_PAGE_URL


uvb_dataset_url = lambda dirname: OC_UVB_BASE_URL.format(dirname=dirname)
#uvb_dataset_url = lambda dirname: f"https://webda.physics.muni.cz/cgi-bin/frame_data_list.cgi?{dirname}+ubv+ubv.peo"
ocl_page_url = lambda dirname: OC_PAGE_URL.format(dirname=dirname)

def get_uvb_response(dirname:str):
    url = uvb_dataset_url(dirname)
    response = requests.get(url)
    return response

def parse_uvb_response_to_df(response:requests.models.Response):
    bs = BeautifulSoup(response.text, "html.parser")
    data_str = bs.find('pre').text
    data_clean = "\n".join([line for line in data_str.splitlines() if line.strip() != ''])
    data_io = io.StringIO(data_clean)
    df = pd.read_fwf(data_io)
    #df_clean = df.dropna().reset_index(drop=True)
    return df

# def extract_hr_bv(df:pd.DataFrame):
#     hr_df = df[['V','B-V']].dropna()
#     return hr_df

def extract_hr_bv(df:pd.DataFrame):
    df = df.rename(columns={'V': 'Mv', 'B-V': 'b_v'})
    hr_df = df[['Mv', 'b_v']].dropna()
    return hr_df


def query_cluster_ubv(cluster_id:str) -> pd.DataFrame:
    response = get_uvb_response(cluster_id)
    cluster_df = parse_uvb_response_to_df(response)
    hr_df = extract_hr_bv(cluster_df)
    return hr_df


def find_alternative_dirname(cluster_id:str) -> str | None:
    page_url = ocl_page_url(cluster_id)
    response = requests.get(page_url)
    bs = BeautifulSoup(response.text, "html.parser")
    table = bs.find('table')
    if table:
        link = table.find("a")
        if link and "dirname=" in link["href"]:
            alt_dirname = link["href"].split("dirname=")[-1]
            return alt_dirname
    return None