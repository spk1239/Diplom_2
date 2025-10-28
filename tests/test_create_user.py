import pytest
import requests
from faker import Faker
from urls import Urls
import allure

class TestCreatingUser():

    @allure.title("Создание пользователя")
    def test_creating_a_user(self):

        fake = Faker(locale="ru_RU") 

        with allure.step("Сгенерировать данные для нового пользователя"):
            payload = {
                       "email": fake.email(),
                       "password": fake.password(),
                       "name": fake.name()
                      }

        with allure.step("Создать нового пользователя"):
            response = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Проверить успешное создание пользователя"):
            assert response.status_code == 200 and ("accessToken" and "refreshToken") in response.json() 

    @allure.title("Создание уже существующего пользователя")
    def test_dont_creating_similar_user(self):

        fake = Faker(locale="ru_RU") 

        with allure.step("Сгенерировать данные для пользователя"):
            payload = {
                       "email": fake.email(),
                       "password": fake.password(),
                       "name": fake.name()
                      }

        with allure.step("Создать первого пользователя"):
            response = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Попытаться создать пользователя с такими же данными"):
            response_second = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Проверить ошибку создания дубликата пользователя"):
            assert response_second.status_code == 403 and response_second.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без одного обязательно поля")
    @pytest.mark.parametrize("data", ["email", "password", "name"])
    def test_dont_creating_user_missing_field(self, data):

        fake = Faker(locale="ru_RU") 

        with allure.step("Сгенерировать данные и удалить одно обязательное поле"):
            payload = {
                       "email": fake.email(),
                       "password": fake.password(),
                       "name": fake.name()
                      }
            del payload[data]

        with allure.step("Попытаться создать пользователя без обязательного поля"):
            response = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Проверить ошибку недостатка данных для создания"):
            assert response.status_code == 403 and response.json()["message"] == "Email, password and name are required fields"