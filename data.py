class TestData:
    # Ингредиенты для заказов
    VALID_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6c", "61c0c5a71d1f82001bdaaa76"]
    INVALID_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6c222", "61c0c5a71d1f82001bуауdaaa76"]
    
    # Сообщения об ошибках
    ERROR_MESSAGES = {
        "INGREDIENTS_REQUIRED": "Ingredient ids must be provided",
        "USER_EXISTS": "User already exists", 
        "FIELDS_REQUIRED": "Email, password and name are required fields",
        "INVALID_CREDENTIALS": "email or password are incorrect"
    }
    
    # Статус коды
    STATUS_CODES = {
        "SUCCESS": 200,
        "BAD_REQUEST": 400,
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
        "SERVER_ERROR": 500
    }