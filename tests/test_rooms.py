import requests
import logging

logger = logging.getLogger(__name__)

def test_get_all_rooms(base_url, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(f"{base_url}/rooms")
        logger.info(f"GET /rooms => {response.status_code}")
        logger.debug(f"Response: {response.text}")
        assert response.status_code == 200
        data = response.json().get("data", [])
        assert isinstance(data, list)

def test_get_room_by_id(base_url, caplog):
    with caplog.at_level(logging.INFO):
        # First get any room
        all_rooms = requests.get(f"{base_url}/rooms").json().get("data", [])
        assert all_rooms, "No rooms available to test"
        room_id = all_rooms[0]["id"]

        # Then fetch it directly
        response = requests.get(f"{base_url}/rooms/{room_id}")
        logger.info(f"GET /rooms/{room_id} => {response.status_code}")
        logger.debug(f"Response: {response.text}")
        assert response.status_code == 200
        room = response.json().get("data", {})
        assert room["id"] == room_id

def test_get_room_invalid_id_returns_404_or_400(base_url, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(f"{base_url}/rooms/invalid-room-id")
        logger.info(f"GET /rooms/invalid-room-id => {response.status_code}")
        assert response.status_code in [400, 404]

def test_get_rooms_by_hotel_id(base_url, caplog):
    with caplog.at_level(logging.INFO):
        hotels = requests.get(f"{base_url}/hotels").json().get("data", [])
        assert hotels, "No hotels found in seed data"
        hotel_id = hotels[0]["id"]

        response = requests.get(f"{base_url}/rooms/hotel/{hotel_id}")
        logger.info(f"GET /rooms/hotel/{hotel_id} => {response.status_code}")
        assert response.status_code == 200
        rooms = response.json().get("data", [])
        assert isinstance(rooms, list)

def test_get_available_rooms(base_url, caplog):
    with caplog.at_level(logging.INFO):
        hotels = requests.get(f"{base_url}/hotels").json().get("data", [])
        assert hotels, "No hotels available"
        hotel_id = hotels[0]["id"]

        response = requests.get(f"{base_url}/rooms/hotel/{hotel_id}/available")
        logger.info(f"GET /rooms/hotel/{hotel_id}/available => {response.status_code}")
        rooms = response.json().get("data", [])
        if rooms:
            logger.info(f"Found {len(rooms)} available rooms")
        else:
            logger.warning("No rooms marked as available — may indicate a seed bug")
        assert response.status_code == 200
        assert isinstance(rooms, list)
