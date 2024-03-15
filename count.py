import pandas as pd
import os
import re
data =  pd.read_csv("./pdf_links/CIF_AND_DOI_DISTINCT_with_links.csv")
data_path = os.path.join(os.getcwd(), "language_struct_project_data")

CIFs = set(os.listdir(data_path))

data["DOWNLOADED"] = 0
#print(CIFs)
for index, row in data[1:].iterrows():
    CIF = re.search(r'\d+',row["CIF_URL"]).group()
    if  CIF in CIFs:
        #print(CIF)
        data.at[index,"DOWNLOADED"] = 1
data.to_csv("DOWNLOADED_CIF_AND_DOI.csv",index=False)