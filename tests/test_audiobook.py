from fastapi.testclient import TestClient
from src.main import app  # Adjust import according to your project structure
from src.models.user_account import User  # Adjust import according to your project structure
from src.database import get_db, SessionLocal
from src.authentication.auth import get_current_user

def override_get_current_user():
    return User(username="test_user", email="abc@gmail.com", password_hash="test_password")

# Dependency override for testing
app.dependency_overrides[get_db] = lambda: SessionLocal()
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_create_audiobook():
    response = client.post(
        "/audiobooks",
        json={
            "title": "Khileya",
            "author": "Mitraz",
            "duration": 10,
            "cover_image_url": "na"
        }
    )

    assert response.status_code == 201

    created_audiobook = response.json()

    assert created_audiobook["title"] == "Khileya"
    assert created_audiobook["author"] == "Mitraz"
    assert created_audiobook["duration"] == 10
    assert created_audiobook["cover_image_url"] == "na"
    assert created_audiobook["is_available"] is True
    assert "id" in created_audiobook
    assert "created_at" in created_audiobook


def test_get_audiobook():
    # First, create an audiobook to retrieve it
    response = client.post(
        "/audiobooks",
        json={
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "duration": 300,
            "cover_image_url": "http://example.com/gatsby.jpg"
        }
    )
    audiobook_id = response.json().get("id")  # Get the ID of the created audiobook

    # Now request to get the audiobook by ID
    response = client.get(f"/audiobooks/{audiobook_id}")

    # Assertions
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby"


def test_update_audiobook():
    # Create an audiobook to update
    create_response = client.post(
        "/audiobooks",
        json={
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "duration": 300,
            "cover_image_url": "http://example.com/gatsby.jpg"
        }
    )
    audiobook_id = create_response.json().get("id")  # Get the ID of the created audiobook

    # Now request to update the audiobook
    response = client.put(
        f"/audiobooks/{audiobook_id}",
        json={
            "title": "The Great Gatsby - Updated",
            "author": "F. Scott Fitzgerald",
            "duration": 360,
            "cover_image_url": "http://example.com/gatsby_updated.jpg"
        }
    )

    # Assertions
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby - Updated"


def test_delete_audiobook():
    # Create an audiobook to delete
    create_response = client.post(
        "/audiobooks",
        json={
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "duration": 300,
            "cover_image_url": "http://example.com/gatsby.jpg"
        }
    )
    audiobook_id = create_response.json().get("id")  # Get the ID of the created audiobook

    # Now request to delete the audiobook
    response = client.delete(f"/audiobooks/{audiobook_id}")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Audiobook deleted successfully"}

