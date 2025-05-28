import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_valid_user_id_returns_recommendations(client):
    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)
    assert len(data) > 0 

def test_missing_user_id_returns_error(client):
    response = client.get("/recommendations")
    assert response.status_code == 400
    assert "error" in response.get_json()
