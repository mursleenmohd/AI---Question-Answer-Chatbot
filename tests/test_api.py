from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert (
        response.json()["message"] == "AI Chatbot API is running"
    )

def test_chat_validation():
    response = client.post(
        "/chat",
        json={
            "message": "",
            "history": [],
        },
    )
    assert response.status_code == 422