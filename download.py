#Download files to temp locations and then check that, if it is there, move it to the special folder and download cif and move it there.
#Then clear the temp folder.
import os
def create_driver(temp):
    from selenium import webdriver
    import time
    options = webdriver.ChromeOptions()
    #Folder download_location determined here.    
    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": temp,
               "download.extensions_to_open": "",
               "plugins.always_open_pdf_externally": True}
    
    options.add_experimental_option("prefs", profile)
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    return driver


def download_pdf(lnk,driver,CIF,temp,data_path):
    import os
    import time
    import re
    #print("Downloading file from link: {}".format(lnk))
    #Make sure to delete any files in temp pre-existing
    for file in os.listdir(temp):
        os.unlink(os.path.join(temp,file))
    driver.get(lnk)
    driver.get(CIF)
    time.sleep(4)
    files_downloaded = os.listdir(temp)
    new_path = os.path.join(os.getcwd(),data_path,re.search(r'\d+',CIF).group())
    #Delete all files originally in new_path.
    if (len(files_downloaded) == 2):
        #Move contents to the other proper directory it should be in.
        #Move CIFS to one path and pdf to another path.
        #First ensure all files download withour crdownload.
        #In the end it will not wait for crdownloads, will first try to download everything cleanly.
        if "crdownload" not in "".join(files_downloaded):
            #Will only make it if it has the data and it exists.
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            for file in files_downloaded:
                os.rename(os.path.join(temp,file),os.path.join(new_path,file))
            #Delete either CIF, or lnk, whichever actually downloaded.
    for file in os.listdir(temp):
        os.unlink(os.path.join(temp,file))
    return driver
if __name__ == "__main__":
    folder_path = os.path.join(os.getcwd(), "temp")
    data_path = os.path.join(os.getcwd(), "language_struct_project")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    temp1 = "C:\\Users\\ankit\\OneDrive\\Documents\\Georgia Tech\\Georgia Tech Spring 2024\\MaterialResearch\\pdfs\\temp"    

    CIF = "https://www.crystallography.net/9016503.cif"
    pdf = "https://www.sciencedirect.com/science/article/pii/S0022459683710030/pdf?md5=4c6441310ba544f391eb2a74b7f4392c&pid=1-s2.0-S0022459683710030-main.pdf"
    download_pdf(pdf,create_driver(temp1),CIF,temp1,data_path)

#Multi-threading ideas
#For downloading
#Open 10 threads and then wait them all.
#I want to make sure I don't use a bunch of drivers repeatadly.