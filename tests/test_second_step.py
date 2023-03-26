from selenium import webdriver
from selenium.webdriver.common.by import By

import pytest


@pytest.fixture(params=["chrome"], scope="function")
def init_driver(request):
    if request.param == 'firefox':
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = True
        web_driver = webdriver.Firefox(options=firefox_options)
    if request.param == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        web_driver = webdriver.Chrome(options=chrome_options)

    yield web_driver

    web_driver.close()


@pytest.mark.usefixtures("init_driver")
def test_login(init_driver):
    init_driver.get("https://ya.ru")
    elem = init_driver.find_element(By.NAME, "lr")

    print("Successuly access {}".format('ya.ru'))