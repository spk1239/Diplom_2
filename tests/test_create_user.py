import pytest
import requests
from faker import Faker
from urls import Urls
import allure
from data import TestData

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
            assert response.status_code == TestData.STATUS_CODES["SUCCESS"]
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()

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
            requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Попытаться создать пользователя с такими же данными"):
            response_second = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Проверить ошибку создания дубликата пользователя"):
            assert response_second.status_code == TestData.STATUS_CODES["FORBIDDEN"]
            assert response_second.json()["message"] == TestData.ERROR_MESSAGES["USER_EXISTS"]

    @allure.title("Создание пользователя без одного обязательно поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_dont_creating_user_missing_field(self, field):
        fake = Faker(locale="ru_RU") 

        with allure.step("Сгенерировать данные и удалить одно обязательное поле"):
            payload = {
                "email": fake.email(),
                "password": fake.password(),
                "name": fake.name()
            }
            del payload[field]

        with allure.step("Попытаться создать пользователя без обязательного поля"):
            response = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)

        with allure.step("Проверить ошибку недостатка данных для создания"):
            assert response.status_code == TestData.STATUS_CODES["FORBIDDEN"]
            assert response.json()["message"] == TestData.ERROR_MESSAGES["FIELDS_REQUIRED"]