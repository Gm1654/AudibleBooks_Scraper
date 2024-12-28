import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# options = Options()
# options.add_argument("--headless")  # Enable headless mode
# options.add_argument("--disable-gpu")  # Disable GPU (for better compatibility in headless mode)
# options.add_argument("--window-size=1920,1080")

web='https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&pf_rd_p=bb0efe44-14ef-41cc-91b0-c1b40e66ffe2&pf_rd_r=AX8FGWMYJ6XWR72A1687&plink=BorxHQ81OmYKcMwk&pageLoadId=tlF3DHgU1aqdnlyR&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482&ref=a_search_t1_navTop_pl0cg1c0r0'
driver=webdriver.Chrome()
driver.get(web)
driver.maximize_window()

pagination = driver.find_element(By.XPATH,'//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.XPATH,'li')
last_page = int(pages[-2].text)

book_title=[]
book_author=[]
book_length=[]


current_page=1
while current_page <= last_page:
    # Implicit Wait
    # time.sleep(2)
    # Explicit Wait
    # container = driver.find_element_by_class_name('adbl-impression-container ')
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    # products = container.find_elements_by_xpath('.//li[contains(@class, "productListItem")]')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]')))

  

    for product in products:
        book_title.append(product.find_element(By.XPATH,'.//h3[contains(@class,"bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH,'.//li[contains(@class,"authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH,'.//li[contains(@class,"runtimeLabel")]').text)

    current_page+=1

    try:
        next_page=driver.find_element(By.XPATH,'//span[contains(@class,"nextButton")]')
        next_page.click()
    except:
        pass    
    
    
driver.quit()

df_books=pd.DataFrame({'Book_title':book_title,'Book_author':book_author,'Book_length':book_length})
df_books.to_csv('BooksData.csv',index=False)

    






















