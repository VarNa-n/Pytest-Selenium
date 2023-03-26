from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


options = Options()
#options.add_argument("--headless")
options.add_argument("no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=800,600")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=options)
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
print(driver.page_source)
#assert "No results found." not in driver.page_source

new_window = driver.switch_to.new_window()
driver.get("http://ya.ru")
sleep(2)

driver.switch_to.window(driver.window_handles[0])
sleep(2)
driver.refresh()
driver.close()
driver.quit()