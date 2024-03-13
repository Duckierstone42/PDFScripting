import pandas as pd
import concurrent.futures
import os
import re
data=  pd.read_csv("./pdf_links/CIF_AND_DOI_DISTINCT_with_links62000.csv")
print("Total entries in data:",len(data))
counter = 0
max_workers = 10
from download import download_pdf, create_driver
current_pool_size=0 #Also indicates unallocated device.
#Create drivers with temp file paths.
temp_paths=[]
main_temp = os.path.join(os.getcwd(),"temp")
if not os.path.exists(main_temp):
     os.mkdir(main_temp)
for i in range(10):
        folder_name = "temp"+str(i)
        folder_path = os.path.join(main_temp,folder_name)
        if os.path.exists(folder_path):
             #Delete all pre-existing contents
             for file in os.listdir(folder_path):
                  os.unlink(os.path.join(folder_path,file))
        else:
             os.makedirs(folder_path)
        temp_paths.append(folder_path)
devices = [create_driver(temp_path) for temp_path in temp_paths]

used_devices = []
pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
data_path = os.path.join(os.getcwd(), "language_struct_project_data")
if not os.path.exists(data_path):
    os.makedirs(data_path)
initial_total = len(os.listdir(data_path))
try:
    for index, row in data.iterrows():
        counter+=1 #It' actually counting even if it wasn't filled yet. 
        if (current_pool_size == max_workers):
            pool.shutdown(wait=True)
            current_pool_size=0
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
            print("Finished current pool")
        data_name = re.search(r'\d+',row["CIF_URL"]).group()
        if (data_name in os.listdir(data_path)):
            file_path = os.path.join(data_path,data_name)
            if (len(os.listdir(file_path)) == 2):
                #Only skips if its a proper folder. 
                counter-=1 
                continue
        #If folder path already exists, that means we've already processed this data, so skip
        if (not pd.isna(row["pdf_link"])):
            pool.submit(download_pdf,row["pdf_link"],devices[current_pool_size],row["CIF_URL"],temp_paths[current_pool_size],data_path)

            current_pool_size+=1
        #How can I speed it up so it in only waits as short as needed.
        if (counter % 100 == 0 and counter != 0):# CHANGE THIS to limit the number of pdf links you want to download at a time.
            num_total = len(os.listdir(data_path))
            print(f"Downloaded {num_total-initial_total} pairs, with {(num_total-initial_total)/counter}, at {index}")
except Exception as e:
    print(e)
    print("Shutting down...")
    pool.shutdown(wait=True)

#Science direct websites appear to fail to work.
pool.shutdown(wait=False)

for device in devices:
    device.quit()
print("Done!")

#Now counter only increments when considering new files.