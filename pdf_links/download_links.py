from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#Create a script that checks every URL from either DOI org and 

# Navigate to the website
def get_pdf_link(doi,used_driver):

    URL = "http://doi.org/" + doi
    driver.get(URL)

    # Find all links on the page
    tries = 3
    for _ in range(tries):
        try:
            # Find all links on the page
            links = used_driver.find_elements(By.TAG_NAME, 'a')
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

# Close the WebDriver
if __name__ == "__main__":    
    doi = "10.1107/S0567740878010444"
    print(get_pdf_link(doi,driver))
    driver.quit()
