import io
import requests
from bs4 import BeautifulSoup
import pandas as pd

from stellar_isochrones.config import OC_UVB_BASE_URL


uvb_dataset_url = lambda dirname: OC_UVB_BASE_URL.format(dirname=dirname)
#uvb_dataset_url = lambda dirname: f"https://webda.physics.muni.cz/cgi-bin/frame_data_list.cgi?{dirname}+ubv+ubv.peo"

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

def extract_hr_bv(df:pd.DataFrame):
    hr_df = df[['V','B-V']].dropna()
    return hr_df