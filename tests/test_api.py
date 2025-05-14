import pytest
from app.main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_valid_recommendation_request(client):
    response = client.post("/recommendations", json={"user_id": 1})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert "event_id" in data[0]
    assert "odds" in data[0]

def test_invalid_recommendation_request(client):
    response = client.post("/recommendations", json={})
    assert response.status_code == 400
