import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR =  os.path.dirname(os.path.abspath(__file__))

################################################################
DATA_DIR = os.path.join(BASE_DIR, "data")

#DEFAULT ZAMS DATA LOCATION
ZAMS_FILE = os.path.join(DATA_DIR, "zams.csv")

#DEFAULT ISOCHRONES DATA LOCATION
ISOCHRONE_DIR = os.path.join(DATA_DIR, "isochrones")
ISOCHRONE_FILE_GLOB_PATTERN = f"{ISOCHRONE_DIR}/*.dat"  
ISOCHRONE_COLUMNS = [
    "Z", "age", "log_age", "M_ini", "M_act", "logL/Lo", "logTe", "logG",
    "Mbol", "Mu", "Mb", "Mv", "Mr", "Mi", "Mj", "Mh", "Mk", "Flum"
]

ISOCHRONE_SCHEMA_LIST = ['Z','log_age','Mv','b_v']
################################################################

#Open Cluster UVB photometry query parameters
OC_LIST_URL = "https://webda.physics.muni.cz/cgi-bin/slm.cgi?ubvpe" 
OC_UVB_BASE_URL="https://webda.physics.muni.cz/cgi-bin/frame_data_list.cgi?{dirname}+ubv+ubv.peo"
LYNGA_CAT_BASE_URL="https://webda.physics.muni.cz/cgi-bin/frame_data_list.cgi?{dirname}+lyn+lyn.dat"

cluster_df_columns = ['id', 'name', 'star_count']

# individual cluster query

#VIZIER catalogue
CLUSTER_CATALOGUE = "B/ocl/clusters"

#ZAMS
#mist_url = "https://waps.cfa.harvard.edu/MIST/iso_form.php"
#ISO_ZIP_BASE_URL = "https://waps.cfa.harvard.edu/MIST/{iso_link}"