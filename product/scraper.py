from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def flipkart_scraper(prod, items):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=webdriver.ChromeOptions(
    ).add_argument('--ignore-certificate-errors'))
    wait = WebDriverWait(driver, 10)

    site = 'https://www.flipkart.com'
    driver.get(site)

    driver.implicitly_wait(10)
    cross_elem = driver.find_element(
        By.XPATH, "//button[@class='_2KpZ6l _2doB4z']")
    cross_elem.click()

    search_elem = driver.find_element(By.NAME, "q")
    search_elem.send_keys(prod)
    search_elem.send_keys(Keys.ENTER)

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[@class='_10Ermr']")))

    soup_searchpage = BeautifulSoup(driver.page_source, 'lxml')

    x = 0

    scraped_products = []

    # print(soup_searchpage.find_all("a", class_="_1fQZEK"))
    for product in soup_searchpage.find_all("a", class_="_1fQZEK", limit=items):
        product_open_button = driver.find_elements(
            By.XPATH, "//a[@class='_1fQZEK']")[x]
        product_open_button.click()
        driver.switch_to.window(driver.window_handles[1])
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[@class='yhB1nd']")))

        soup_productpage = BeautifulSoup(driver.page_source, 'lxml')
        product_name = soup_productpage.body.find(
            "span", class_="B_NuCI").get_text().split('-')[0]
        product_price = soup_productpage.body.find(
            "div", class_="_30jeq3 _16Jk6d").get_text()
        product_price = int((product_price.lstrip('₹')).replace(',', ''))
        product_details = {
            'title': product_name,
            'price': product_price
        }
        scraped_products.append(product_details)

        driver.execute_script("window.close()")
        driver.switch_to.window(driver.window_handles[0])
        x += 1

    # print(scraped_products)
    return scraped_products
