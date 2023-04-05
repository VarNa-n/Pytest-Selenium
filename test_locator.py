from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('/ChromeDrv/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   #sleep(3)
   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('nata@varsh.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('1q2w3')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends", "Main page"


   my_pets = pytest.driver.find_element(By.LINK_TEXT, u"Мои питомцы")
   my_pets.click()


   # Кол-во питомцев
   count_my_pets_str = pytest.driver.find_element(By.CSS_SELECTOR, 'div.col-sm-4.left > h2')
   print("\n", count_my_pets_str, "\n")
   # Фото
   images = pytest.driver.find_elements(By.XPATH, '//img[contains(@src, "data:image")]')

   count_my_pets = len(images)

   for i in range(len(images)):
      assert images[i].get_attribute('src') != ''
