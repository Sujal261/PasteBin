import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import initialize_db, get_db_connection

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Initialize the database before running tests
    initialize_db()
    yield
    # Optional teardown: clear table after tests
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pastes")
    conn.commit()
    conn.close()

def test_create_paste():
    response = client.post("/create/", params={
        "content": "Hello, world!",
        "user_id": "user123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "url_id" in data
    assert "url" in data
    global test_url_id
    test_url_id = data["url_id"]

def test_view_paste_without_password():
    response = client.get(f"/view/{test_url_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, world!"
    assert data["user_id"] == "user123"

def test_get_info():
    response = client.get(f"/info/{test_url_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user123"
    assert "created_at" in data
    assert "expires_at" in data
    assert data["is_expired"] is False

def test_create_paste_with_password_and_wrong_access():
    response = client.post("/create/", params={
        "content": "Secret paste",
        "user_id": "user456",
        "password": "secure123"
    })
    assert response.status_code == 200
    protected_url_id = response.json()["url_id"]

    # Try accessing without password
    response = client.get(f"/view/{protected_url_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Password required or incorrect"

    # Try accessing with wrong password
    response = client.get(f"/view/{protected_url_id}", params={"password": "wrong"})
    assert response.status_code == 403

    # Access with correct password
    response = client.get(f"/view/{protected_url_id}", params={"password": "secure123"})
    assert response.status_code == 200
    assert response.json()["content"] == "Secret paste"
