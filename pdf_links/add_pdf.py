import pandas as pd
import numpy as np
pairs_frame = pd.read_csv("./CIF_AND_DOI_DISTINCT_with_links.csv")
initial_length = len(pairs_frame)
pairs_frame.head()
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
# Initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=service,options=chrome_options)
driver.implicitly_wait(1)
def get_pdf_link(doi):

    URL = "http://doi.org/" + doi
    driver.get(URL)
    # Find all links on the page
    tries = 3
    for _ in range(tries):
        try:
            # Find all links on the page
            links = driver.find_elements(By.TAG_NAME, 'a')
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

    # Print the PDF links
    if len(pdf_links) == 0:
        return None
    else:
        return pdf_links[0]

count = 0
total = 0
total_in_file=0
try:
    for index, row in pairs_frame.iloc[45309:].iterrows():
        if (pd.isna(row["pdf_link"])):
            print(index)
            total+=1
            try:
                result = get_pdf_link(row["DOI"])
            except KeyboardInterrupt:
                raise
            except:
                result = None
            if result != None:
                count+=1
                pairs_frame.at[index,"pdf_link"] = result
        total_in_file+=1
        if (index % 100 == 0):
            print(f"Sucesses: {count}")
            print(f"Total Attempts: {total}")
            print(f"Total DOI's traversed {total_in_file}")
        if (index % 100 == 0 and index != 0):
            #Save current df
            pairs_frame.to_csv(f"./CIF_AND_DOI_DISTINCT_with_links{(index // 1000) * 1000}.csv", index=False)
except:
    #Ensures that we will save our data regardless of what else happens.
    if (len(pairs_frame)) == initial_length:
        pairs_frame.to_csv("./CIF_AND_DOI_DISTINCT_with_links.csv", index=False)
    print("Success Rate:",count/total)
    print("Hit Rate:",count)
    print("Total pdf links: ",total)
    print("DOIs skipped cuz already acquired:",total_in_file-count)
if (len(pairs_frame)) == initial_length:
    pairs_frame.to_csv("./CIF_AND_DOI_DISTINCT_with_links.csv", index=False)


#Two main websites that contain a lot of articles that are failing

#pubs.acs
#science direct.