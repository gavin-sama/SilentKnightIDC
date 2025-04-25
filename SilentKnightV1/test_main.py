from fastapi.testclient import TestClient
from loginFastAPI import app  # replace with the filename where your FastAPI app lives

client = TestClient(app)

# <summary>
# Tests user creation with sample credentials and checks for success or duplication.
# </summary>
def test_create_user():
    response = client.post("/users", json={
        "username": "testuser",
        "password": "testpass",
        "encryption": 3
    })
    assert response.status_code == 200 or response.status_code == 400  # in case the user already exists

# <summary>
# Retrieves all users and verifies the response is a list with HTTP 200 status.
# </summary>
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# <summary>
# Fetches encryption level for a user and ensures the result is numeric.
# </summary>
def test_get_encryption():
    response = client.get("/encryption/testuser")
    assert response.status_code == 200
    assert response.text.isdigit()

# <summary>
# Sends a message and verifies it can be retrieved successfully.
# </summary>
def test_send_and_fetch_message():
    # Send a message
    response = client.post("/send_message", json={
        "sender": "testuser",
        "receiver": "testuser",
        "message": "Hello!"
    })
    assert response.status_code == 200

    # Get the message
    response = client.get("/messages/testuser")
    assert response.status_code == 200
    assert any("Hello!" in msg["message"] for msg in response.json())

# <summary>
# Deletes all messages for the given user and checks for successful deletion.
# </summary>
def test_delete_messages():
    response = client.post("/delete_messages", params={"receiver": "testuser"})
    assert response.status_code == 200 or response.status_code == 204

# <summary>
# Deletes a user and validates that the deletion was successful.
# </summary>
def test_delete_user():
    response = client.post("/delete_user", params={"username": "testuser"})
    assert response.status_code == 200 or response.status_code == 204

########## ANYTHING BELOW THIS LINE SHOULD FAIL THE TEST. 

# <summary>
# Attempts to retrieve encryption for a user who doesn't exist.
# Should return a 404 Not Found or similar error. Useful to show that tests CAN fail and to test for bugs 
# where encryption can occur randomly. 
# </summary>
def test_get_encryption_non_existent_user():
    response = client.get("/encryption/nonexistentuser")
    assert response.status_code == 404  





