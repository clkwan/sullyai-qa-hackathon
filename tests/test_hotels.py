import requests
import logging

logger = logging.getLogger(__name__)

def test_list_hotels(base_url, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(f"{base_url}/hotels")
        logger.info(f"Response body: {response.text}")
    assert response.status_code == 200

def test_get_hotel_invalid_id(base_url, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(f"{base_url}/hotels/invalid_id")
        logger.info(f"Response body: {response.text}")
    assert response.status_code in (400, 404)
