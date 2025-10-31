import pytest
import requests
from urls import Urls
import allure
from data import TestData

class TestCreatingOrder():
    
    @allure.title("Создание заказа авторизированным пользователем")
    def test_creating_order_by_an_login_user(self, login_user):
        with allure.step("Создать заказ авторизированным пользователем"):
            payload = {"ingredients": TestData.VALID_INGREDIENTS}
            response = requests.post(f'{Urls.BURGER_URL}/api/orders', data=payload,
                                   headers={"Authorization": login_user["accessToken"]})
            
        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == TestData.STATUS_CODES["SUCCESS"]
            assert response.json()["success"] == True

    @allure.title("Создание заказа не авторизированным пользователем")
    def test_creating_order_by_no_login_user(self):
        with allure.step("Создать заказ пользователем"):
            payload = {"ingredients": TestData.VALID_INGREDIENTS}
            response = requests.post(f'{Urls.BURGER_URL}/api/orders', data=payload)

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == TestData.STATUS_CODES["SUCCESS"]
            assert response.json()["success"] == True

    @allure.title("Создание заказа без ингридиентов")
    def test_creating_order_by_not_ingredients(self):
        with allure.step("Создать заказ пользователем"):
            response = requests.post(f'{Urls.BURGER_URL}/api/orders', data={})

        with allure.step("Проверить ошибку заказа"):
            assert response.status_code == TestData.STATUS_CODES["BAD_REQUEST"]
            assert response.json()["message"] == TestData.ERROR_MESSAGES["INGREDIENTS_REQUIRED"]

    @allure.title("Создание заказа c неправильным хэшем ингридиентов")
    def test_creating_order_by_invalid_hash(self):
        with allure.step("Создать заказ пользователем"):
            payload = {"ingredients": TestData.INVALID_INGREDIENTS}
            response = requests.post(f'{Urls.BURGER_URL}/api/orders', data=payload)

        with allure.step("Проверить ошибку заказа"):
            assert response.status_code == TestData.STATUS_CODES["SERVER_ERROR"]