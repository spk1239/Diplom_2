import pytest
import requests
from urls import Urls
import allure

class TestCreatingOrder():
    
    @allure.title("Создание заказа авторизированным пользователем")
    def test_creating_order_by_an_login_user(self, login_user):

        with allure.step("Вход авторизированным пользователем"):
            user = login_user
        
        with allure.step("Создать заказ авторизированным пользователем"):
            payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6c","61c0c5a71d1f82001bdaaa76"]}

            response = requests.post(f'{Urls.BURGER_URL}/api/orders',  data=payload,
                                     headers={"Authorization": user["accessToken"]})
            
        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200 and response.json()["success"] == True

    @allure.title("Создание заказа не авторизированным пользователем")
    def test_creating_order_by_no_login_user(self):
        
        with allure.step("Создать заказ пользователем"):
            payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6c","61c0c5a71d1f82001bdaaa76"]}

            response = requests.post(f'{Urls.BURGER_URL}/api/orders',  data=payload)


        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200 and response.json()["success"] == True

    @allure.title("Создание заказа c ингридиентами")
    def test_creating_order_by_ingredients(self):
        
        with allure.step("Создать заказ пользователем"):
            payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6c","61c0c5a71d1f82001bdaaa76"]}

            response = requests.post(f'{Urls.BURGER_URL}/api/orders',  data=payload)


        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200 and response.json()["success"] == True

    @allure.title("Создание заказа без ингридиентов")
    def test_creating_order_by_not_ingredients(self):
        
        with allure.step("Создать заказ пользователем"):
            payload = {}

            response = requests.post(f'{Urls.BURGER_URL}/api/orders',  data=payload)


        with allure.step("Проверить ошибку заказа"):
            assert response.status_code == 400 and response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа c неправильным хэшем ингридиентов")
    def test_creating_order_by_invalid_hash(self):
        
        with allure.step("Создать заказ пользователем"):
            payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6c222","61c0c5a71d1f82001bуауdaaa76"]}

            response = requests.post(f'{Urls.BURGER_URL}/api/orders',  data=payload)


        with allure.step("Проверить ошибку заказа"):
            assert response.status_code == 500