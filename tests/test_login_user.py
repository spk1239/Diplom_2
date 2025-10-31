import pytest
import requests
from urls import Urls
import allure
from faker import Faker
from data import TestData

class TestCourierLogin():

    @allure.title('Проверка Входа зарегистрированного пользователя')
    def test_courier_login_user(self, registered_user):
        with allure.step("Выполнить вход зарегистрированного пользователя"):
            response = requests.post(f"{Urls.BURGER_URL}/api/auth/login", data=registered_user)

        with allure.step("Проверить успешный вход"):
            assert response.status_code == TestData.STATUS_CODES["SUCCESS"]
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()
    
    @allure.title('Проверка Входа при неверном логине и пароле')
    @pytest.mark.parametrize("field", ["email", "password"])
    def test_user_login_without_invalid_login_and_password(self, field, registered_user):
        fake = Faker(locale="ru_RU") 

        with allure.step("Замена логина и пароля на несуществующий"):
            payload = registered_user.copy()
            payload[field] = fake.email()

        with allure.step("Попытаться выполнить вход c неверным логином и паролем"):
            response = requests.post(f"{Urls.BURGER_URL}/api/auth/login", data=payload)

        with allure.step("Проверить ошибку ненайденной учетной записи"):
            assert response.status_code == TestData.STATUS_CODES["UNAUTHORIZED"]
            assert response.json()['message'] == TestData.ERROR_MESSAGES["INVALID_CREDENTIALS"]