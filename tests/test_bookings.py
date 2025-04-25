import requests
import logging
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def test_create_booking_missing_fields(base_url, caplog):
    with caplog.at_level(logging.INFO):
        payload = {
        # intentionally missing required fields
        }
        response = requests.post(f"{base_url}/bookings", json=payload)
        logger.info(f"Response body: {response.text}")
    assert response.status_code in (400, 422)

def test_get_booking_not_found(base_url, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(f"{base_url}/bookings/invalid_booking_id")
        logger.info(f"Response body: {response.text}")
    assert response.status_code in (404,400)

def test_create_valid_booking_with_seed_data(base_url, caplog):
    with caplog.at_level(logging.INFO):
        # Step 1: Get an existing user
        users_res = requests.get(f"{base_url}/users")
        logger.info(f"Users response: {users_res.status_code} - {users_res.text}")
        assert users_res.status_code == 200
        users = users_res.json().get("data", [])
        assert users, "No users found in seed data."
        user_id = users[0]["id"]
        logger.info(f"Using existing user ID: {user_id}")

        # Step 2: Get an existing hotel
        hotels_res = requests.get(f"{base_url}/hotels")
        logger.info(f"Hotels response: {hotels_res.status_code} - {hotels_res.text}")
        assert hotels_res.status_code == 200
        hotels = hotels_res.json().get("data", [])
        assert hotels, "No hotels found in seed data."
        hotel_id = hotels[0]["id"]
        logger.info(f"Using existing hotel ID: {hotel_id}")

        # Step 3: Get an existing available room for that hotel
        rooms_res = requests.get(f"{base_url}/rooms/hotel/{hotel_id}/available")
        logger.info(f"Rooms response: {rooms_res.status_code} - {rooms_res.text}")
        assert rooms_res.status_code == 200
        rooms = rooms_res.json().get("data", [])
        assert rooms, "No available rooms found in seed data for hotel."
        room_id = rooms[0]["id"]
        logger.info(f"Using existing room ID: {room_id}")

        # Step 4: Make a booking
        check_in = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        check_out = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d")
        booking_payload = {
            "user_id": user_id,
            "room_id": room_id,
            "check_in_date": check_in,
            "check_out_date": check_out
        }
        booking_res = requests.post(f"{base_url}/bookings", json=booking_payload)
        logger.info(f"Booking response: {booking_res.status_code} - {booking_res.text}")
        assert booking_res.status_code == 201
        booking_data = booking_res.json().get("data", {})
        assert booking_data.get("user_id") == user_id
        assert booking_data.get("room_id") == room_id
        assert booking_data.get("check_in_date") == check_in
        assert booking_data.get("check_out_date") == check_out

# def test_booking_invalid_date_range(base_url, caplog):
#     with caplog.at_level(logging.INFO):
#         # Get valid user, hotel, and room from seed
#         user_id = requests.get(f"{base_url}/users").json()["data"][0]["id"]
#         hotel_id = requests.get(f"{base_url}/hotels").json()["data"][0]["id"]
#         room_id = requests.get(f"{base_url}/rooms/hotel/{hotel_id}/available").json()["data"][0]["id"]

#         # Set check-out before check-in
#         check_in = (datetime.today() + timedelta(days=5)).strftime("%Y-%m-%d")
#         check_out = (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")

#         payload = {
#             "user_id": user_id,
#             "room_id": room_id,
#             "check_in_date": check_in,
#             "check_out_date": check_out
#         }

#         response = requests.post(f"{base_url}/bookings", json=payload)
#         logger.info(f"Booking response for invalid date range: {response.status_code} - {response.text}")

#         # BUG: Expected 400 but may pass or 500
#         assert response.status_code in [400, 422], "Booking with invalid date range should fail"

# def test_booking_with_room_from_wrong_hotel(base_url, caplog):
#     with caplog.at_level(logging.INFO):
#         # Get a user
#         user_id = requests.get(f"{base_url}/users").json()["data"][0]["id"]

#         # Get 2 hotels
#         hotels = requests.get(f"{base_url}/hotels").json()["data"]
#         assert len(hotels) >= 2, "Need at least 2 hotels to test this"
#         hotel_id_1 = hotels[0]["id"]
#         hotel_id_2 = hotels[1]["id"]

#         # Get a room from hotel 1
#         rooms = requests.get(f"{base_url}/rooms/hotel/{hotel_id_1}/available").json()["data"]
#         assert rooms, "No available rooms for hotel 1"
#         room_id = rooms[0]["id"]

#         # Try to book room from hotel 1, pretending it's part of hotel 2
#         check_in = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
#         check_out = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d")

#         booking_payload = {
#             "user_id": user_id,
#             "room_id": room_id,
#             "check_in_date": check_in,
#             "check_out_date": check_out
#         }

#         response = requests.post(f"{base_url}/bookings", json=booking_payload)
#         logger.info(f"Booking with room-hotel mismatch response: {response.status_code} - {response.text}")

#         # BUG: Should fail because room doesn't belong to selected hotel
#         # But may pass due to lack of validation
#         assert response.status_code != 201, "Booking should fail if room is from a different hotel"
