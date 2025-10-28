import pytest
import requests
from urls import Urls
import allure
from faker import Faker

class TestCourierLogin():

    @allure.title('Проверка Входа зарегистрированного пользователя')
    def test_courier_login_registered_courier(self, registered_user):
        
        user_data = registered_user

        with allure.step("Выполнить вход зарегистрированного пользователя"):
            response = requests.post(f"{Urls.BURGER_URL}/api/auth/login", data=user_data)

        with allure.step("Проверить успешный вход"):
            assert response.status_code == 200 and ("accessToken" and "refreshToken") in response.json()
    
    @allure.title('Проверка Входа при неверном логине и пароле')
    @pytest.mark.parametrize("data", ["email", "password"])
    def test_courier_login_without_invalid_login_and_password(self,data,registered_user):

        fake = Faker(locale="ru_RU") 

        with allure.step("Замена логина и пароля на несуществующий"):
            payload = registered_user
            payload[data] = fake.email

        with allure.step("Попытаться выполнить вход c неверным логином и паролем"):
            response = requests.post(f"{Urls.BURGER_URL}/api/auth/login", data=payload)

        with allure.step("Проверить ошибку ненайденной учетной записи"):
            assert response.status_code == 401 and response.json()['message'] == "email or password are incorrect"