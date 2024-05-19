import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome(options=Options())


def anbima_scraper(ticker, url):
    driver.get(url)
    time.sleep(5)
    pu_op = {}
    temp_data = {}
    juros = {}

    button = driver.find_element(By.XPATH,
                                 '//*[@id="card-calcular-precificacao"]/article/article/section/div'
                                 '/form/div[3]/button')
    button.click()

    time.sleep(5)

    element = driver.find_element(By.XPATH, '//*[@id="card-resultado-precificacao"]/article/article/section'
                                            '/div/div[2]/div[2]/dl/dd')
    pu_op.update({"PU Operação": element.text.replace("R$ ", "")})
    temp_data.update(pu_op)

    table_data = driver.find_element(By.XPATH,
                                     '//*[@id="card-fluxo-pagamento"]/article/article/section/div/div/table/tbody')

    for tr in table_data.find_elements(By.XPATH, "//tr"):
        row = [item.text for item in tr.find_elements(By.XPATH, ".//td")]
        if len(row) == 0 or row[0] != "Juros":
            continue
        else:
            juros.update({row[1].replace(row[1][0:2], "01"): row[5]})
    temp_data.update(juros)
    return temp_data


def exception_scraper(ticker):
    url = "https://calculadorarendafixa.com.br/#/navbar/calculadora"
    driver.get(url)

    pu_op = {}
    temp_data = {}
    juros = {}

    time.sleep(5)

    ActionChains(driver) \
        .scroll_by_amount(0, 600) \
        .perform()
    time.sleep(5)

    if len(ticker) == 6:
        button = driver.find_element(By.XPATH, '//*[@id="tabDebentures"]')
        button.click()
    elif ticker[:3] == "CRI":
        button = driver.find_element(By.XPATH, '//*[@id="tabCRI"]')
        button.click()
    else:
        button = driver.find_element(By.XPATH, '//*[@id="tabCRA"]')
        button.click()

    select_element = driver.find_element(By.XPATH, '//*[@id="codigoTitulo"]')
    select = Select(select_element)
    time.sleep(5)
    select.select_by_value(ticker)

    time.sleep(5)
    button = driver.find_element(By.XPATH, '//*[@id="seletor"]/form/div/div[5]/a/img')
    button.click()
    time.sleep(3)

    wait = WebDriverWait(driver, 10)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-navbar/div/app-calculadora/div[2]/div/div[1]/div/div/div/div/button[1]')))
    button.click()

    time.sleep(5)

    element = driver.find_element(By.XPATH, '/html/body/app-root/app-navbar/div/app-calculadora/div[2]/section[3]/div[1]/div[7]/p/span')
    pu_op.update({"PU Operação": element.text})
    temp_data.update(pu_op)

    table_data = driver.find_element(By.XPATH,
                                         '/html/body/app-root/app-navbar/div/app-calculadora/div[2]/section[3]/div[5]/table')

    for tr in table_data.find_elements(By.XPATH, "//tr"):
        row = [item.text for item in tr.find_elements(By.XPATH, ".//td")]
        if len(row) == 0 or row[1] != "J":
            continue
        else:
            juros.update({row[0]: row[4]})
    temp_data.update(juros)
    return temp_data


def scraper_main(tickers):
    final_data = {}
    for ticker in tickers:
        temp_data = {}
        try:
            if len(ticker) == 6:
                url = "https://data.anbima.com.br/ferramentas/calculadora/debentures/{}".format(ticker)
                temp_data = anbima_scraper(ticker, url)

            else:
                url = "https://data.anbima.com.br/ferramentas/calculadora/certificado-de-recebiveis/{}".format(ticker)
                temp_data = anbima_scraper(ticker, url)

        except:
            #temp_data = exception_scraper(ticker)
            pass

        final_data.update({ticker: temp_data})

    return final_data


#print(scraper_main())
# d = {"ABCD11": {"PU Operação": "1321.83", "01/01/2025": "R$9,25", "01/02/2025": "10,37"},
#      "EFGH11": {"PU Operação": "1321.83", "01/03/2025": "7,89", "01/04/2025": "3,37"}}
