import pytest
import requests
from faker import Faker
from urls import Urls

@pytest.fixture
def registered_user():

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