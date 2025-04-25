# 📃 BUGS.md

## Postman API Findings

---

## 🔍 BUG1: Get Hotel by ID Queries Incorrect Path

- **Category**: API Design / URL Structure
- **Endpoint**: `GET /hotels/{id}`
- **Steps to Reproduce**:
  ```bash
  GET /api/hotels/hotel-001
  ```
- **Expected Behavior**: IDs should be numeric (e.g., `/api/hotels/1`, `/api/hotels/2`)
- **Actual Behavior**: API tries to resolve `hotel-001` as an ID, which leads to invalid behavior.
- **Severity**: Medium
- **Impact**: Breaks standard RESTful patterns and creates unnecessary routing errors.
- **Proposed Fix**: Validate ID inputs to ensure only numeric IDs are accepted; reject or return `400 Bad Request` otherwise.

---

## 🔍 BUG2: Duplicate User Email Not Clearly Handled

- **Category**: Business Logic / Validation
- **Endpoint**: `POST /users`
- **Steps to Reproduce**:
  - Register a user with:
    ```json
    {
      "first_name": "Test",
      "last_name": "User",
      "email": "test@example.com",
      "phone": "1234567890"
    }
    ```
  - Try registering again with the same email.
- **Expected**: `409 Conflict` or validation error with clear message.
- **Actual**: Returns `409`, but error message is unclear and lacks specific feedback.
- **Severity**: Medium
- **Impact**: Client cannot distinguish between "duplicate email" vs "bad input" errors.
- **Proposed Fix**:
  - Return a detailed error message:
    ```json
    { "error": "Email already in use" }
    ```

---

## 🔍 BUG3: Get Rooms Available Always Returns Same Data

- **Category**: Business Logic / Filtering
- **Endpoint**: `GET /rooms?hotelId=<id>&available=<true|false>`
- **Steps to Reproduce**:
  - Call:
    ```http
    GET {{baseUrl}}/rooms?hotelId=1&available=false
    ```
  - Then call:
    ```http
    GET {{baseUrl}}/rooms?hotelId=999&available=true
    ```
  - Observe that both calls return the same response, ignoring filter values.
- **Expected**: API should respect query parameters:
  - Return rooms filtered by `hotelId`
  - Return rooms filtered by `is_available` status
- **Actual**: Response is always the same hardcoded room list:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "hotel_id": 1,
        "room_number": "101",
        "room_type": "Deluxe",
        "price_per_night": 200,
        "is_available": 0,
        "created_at": "2025-04-25T16:58:10",
        "updated_at": "2025-04-25T18:00:26"
      }
    ],
    "message": "Rooms retrieved successfully"
  }
  ```
- **Severity**: High
- **Impact**:
  - Filtering logic completely broken
  - Booking processes depending on room availability fail silently
  - Misleads API consumers by presenting invalid data
- **Proposed Fix**:
  - Correct the query implementation:
    ```sql
    SELECT * FROM rooms WHERE hotel_id = ? AND is_available = ?
    ```
  - Validate and parse query parameters properly
  - Add integration tests specifically for filtering behavior

