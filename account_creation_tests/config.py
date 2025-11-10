BASE_URL = "http://localhost:8080"
API_PREFIX = "/api"

ENDPOINTS = {
    "register": f"{API_PREFIX}/auth/register",
    "login": f"{API_PREFIX}/auth/login",
    "user": f"{API_PREFIX}/users"
}

REQUEST_TIMEOUT = 30

HTTP_STATUS = {
    "success": 200,
    "created": 201,
    "bad_request": 400,
    "unauthorized": 401,
    "not_found": 404,
    "conflict": 409
}

PASSWORD_REQUIREMENTS = {
    "min_length": 8,
    "requires_letter": True,
    "requires_number": True
}
