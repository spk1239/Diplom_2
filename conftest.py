import pytest
import requests
from faker import Faker
from urls import Urls

@pytest.fixture
def registered_user():
    """Фикстура для регистрации пользователя"""
    fake = Faker()
    payload = {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.name()
    }
    
    response = requests.post(f'{Urls.BURGER_URL}/api/auth/register', data=payload)
    

    return {
            "email": payload["email"],
            "password": payload["password"]
        }

@pytest.fixture
def login_user(registered_user):
    """Фикстура для авторизации пользователя и получения токенов"""
        
    user_data = registered_user

    response = requests.post(f"{Urls.BURGER_URL}/api/auth/login", data=user_data)

    return {"accessToken": response.json()["accessToken"],
            "refreshToken": response.json()["refreshToken"]}