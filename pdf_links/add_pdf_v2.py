import pandas as pd
import numpy as np
import concurrent.futures
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
#Doesn't properly work, finds the links but its slow and it doesn't properly save the data.
CONCURRENT = 10
# Initialize Chrome WebDrivers
def create_driver():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=service,options=chrome_options)
    return driver
#Grab and return pdf_link
def get_pdf_link(doi,curr_driver):
    try:

        URL = "http://doi.org/" + doi
        curr_driver.get(URL)
        # Find all links on the page
        tries = 3
        for _ in range(tries):
            try:
                # Find all links on the page
                links = curr_driver.find_elements(By.TAG_NAME, 'a')
                break
            except StaleElementReferenceException:
                pass
        else:
            print("Failed to retrieve links after {} tries".format(tries))
            return None

        # Filter out links that point to PDF files
        pdf_links = []
        for link in links:
            try:
                href = link.get_attribute('href')
                if href and "pdf" in href:
                    pdf_links.append(href)
            except StaleElementReferenceException:
                pass

        # Return pdf_links
        if len(pdf_links) == 0:
            return None
        else:
            return (pdf_links[0])
    except:
        return None


#Concurrency doesnt make it much faster for add_pdf.

pairs_frame = pd.read_csv("./CIF_AND_DOI_DISTINCT_with_links.csv")
print(f"Creating {CONCURRENT} chrome drivers. This tends to take a bit to setup." )
drivers = [create_driver() for _ in range(CONCURRENT)]
current_threads = 0
pool = concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT)
results = [ 0 for _ in range(CONCURRENT)] #Represents future values of each worker.
count = 0
total = 0
total_in_file=0
print("Starting!!!")
try:
    for index, row in pairs_frame.iloc[10000:].iterrows():

        if (current_threads == CONCURRENT):
            pool.shutdown(wait=True)
            current_threads = 0
            for result in results:
                total+=1
                
                if result[1] != None:
                    print(result[0])
                    count+=1
                    pairs_frame.at[result[0],"pdf_link"] = result[1]
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT)
            if (index % 100 == 0):
                print(f"Sucesses: {count}")
                print(f"Total Attempts: {total}")
                print(f"Total DOI's traversed {total_in_file}")

        if (pd.isna(row["pdf_link"])):
            results[current_threads] = (index,pool.submit(get_pdf_link(row["DOI"],drivers[current_threads])))
            current_threads+=1
        total_in_file+=1

except Exception as e:
    pool.shutdown(wait=False)
    print(e)
    #Ensures that we will save our data regardless of what else happens.

    pairs_frame.to_csv("./CIF_AND_DOI_DISTINCT_with_links.csv", index=False)
    raise e

pairs_frame.to_csv("./CIF_AND_DOI_DISTINCT_with_links.csv", index=False)


#Two main websites that contain a lot of articles that are failing

#pubs.acs
#science direct.
#later on work on this and tr to get it better