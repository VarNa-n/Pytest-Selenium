from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True, scope='session')
def testing():
   pytest.driver = webdriver.Chrome('/ChromeDrv/chromedriver.exe')
   pytest.driver.set_window_size(1400, 1000)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   sleep(3)
   pytest.driver.quit()


def test_show_my_pets():
   """Проверка перехода на страницу "Мои питомцы" """

   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('nata@varsh.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('1q2w3')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends", "Main page"

   sleep(3)

   my_pets = pytest.driver.find_element(By.LINK_TEXT, u"Мои питомцы")
   my_pets.click()


def test_count_my_pets():
   """Поверка того, что на странице "Мои питомцы" общее количество питомцев равно числу питомцев в таблице"""

   # Сюда потом можно добавить авторизацию, если не та ссылка
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', "Failed path"

   # Кол-во питомцев
   account_summary = pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text
   count_pets = int(account_summary.split("\n")[1].split(" ")[1])
   print(f"\ncount_pets = {count_pets}")

   # Питомцы в таблице
   count_pets_in_table = len(pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr'))
   print(f"\ncount_pets_in_table = {count_pets_in_table}")

   assert count_pets == count_pets_in_table, "Summary count of pets is not equal the count in the table "


def test_count_photo():
   """Поверка того, что на странице "Мои питомцы" у половины и более питомцев есть фото"""

   # Сюда потом можно добавить авторизацию, если не та ссылка
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', "Failed path"

   pets_in_table = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
   count_pets_in_table = len(pets_in_table)

   # Фото
   images = pytest.driver.find_elements(By.XPATH, '//img[contains(@src, "data:image")]')
   count_my_pets_image = len(images)
   print(f"\nImages = {count_my_pets_image}")

   assert count_my_pets_image / count_pets_in_table > 0.5, "Too few photos"


def test_pet_params():
   """Поверка того, что на странице "Мои питомцы" у всех питомцев есть имя, возраст и порода"""

   # Сюда потом можно добавить авторизацию, если не та ссылка
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', "Failed path"

   pets_in_table = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   for i in range(len(pets_in_table)):
      name, breed, age = pets_in_table[i].text.split("\n")[0].split(" ")
      print("\n", name, breed, age)

      # Проверка имени
      assert name != '', f"{i} pet's name is empty"
      # Проверка породы
      assert breed != '', f"{i} pet's breed is empty"
      # Проверка возраста
      assert age != '', f"{i} pet's age is empty"


def test_different_names():

   """Поверка того, что на странице "Мои питомцы" у всех питомцев разные клички"""

   # Сюда потом можно добавить авторизацию, если не та ссылка
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', "Failed path"

   pets_in_table = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   name_list = set()
   for i in range(len(pets_in_table)):
      name, breed, age = pets_in_table[i].text.split("\n")[0].split(" ")
      print("\n", name, breed, age)
      assert name not in name_list, f"{i} pet's name {name} is not unique"
      name_list.add(name)

def test_different_pets():

   """Поверка того, что на странице "Мои питомцы" у все питомцы разные"""

   # Сюда потом можно добавить авторизацию, если не та ссылка
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', "Failed path"

   pets_in_table = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   pet_list = set()
   for i in range(len(pets_in_table)):
      name, breed, age = pets_in_table[i].text.split("\n")[0].split(" ")
      pet = name + "|" + breed + "|" + age
      print("\n", pet)
      assert pet not in pet_list, f"{i} pet {pet} is not unique"
      pet_list.add(pet)
