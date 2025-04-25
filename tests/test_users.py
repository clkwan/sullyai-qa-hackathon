import requests
import uuid
import logging

logger = logging.getLogger(__name__)

def test_register_user_success(base_url, caplog):
    with caplog.at_level(logging.INFO):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"testuser+{uuid.uuid4().hex[:6]}@example.com",
            "phone": "1234567890"
        }
        logger.info(f"Creating user with payload: {payload}")
        response = requests.post(f"{base_url}/users", json=payload)
        logger.info(f"Received status code: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
    assert response.status_code == 201

def test_get_user_invalid_id(base_url, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(f"{base_url}/users/invalid_id")
        logger.info(f"Response body: {response.text}")
    assert response.status_code in (400, 404)
