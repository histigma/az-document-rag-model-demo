from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/rag/chat", json={"question": 'Hello'})
    print(response.json())
    assert response.status_code == 200
    assert 'message' in response.json()

