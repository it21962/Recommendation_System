import pytest
from unittest.mock import patch, MagicMock
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

#  /recommendations [POST] 

def test_get_recommendations_invalid_algorithm(client):
    payload = {
        "user_id": 1,
        "sport": "football",
        "algorithm": "unknown_algo"
    }
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 400
    assert "Unknown algorithm" in response.get_data(as_text=True)

def test_get_recommendations_invalid_payload(client):
    response = client.post("/recommendations", json={"user_id": "not_int"})
    assert response.status_code == 400
    assert "error" in response.get_json()

@patch("app.main.get_generator")
def test_get_recommendations_success(mock_get_gen, client):
    mock_gen = MagicMock(return_value=[MagicMock(dict=lambda: {"event_id": "e1"})])
    mock_get_gen.return_value = mock_gen

    payload = {
        "user_id": 1,
        "sport": "football",
        "algorithm": "test_algo"
    }

    response = client.post("/recommendations", json=payload)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

#  /recommendations [GET] 

@patch("app.main.get_user_company")
@patch("app.main.get_display_config")
@patch("app.main.get_dynamic_recommendations")
def test_fetch_dynamic_recommendations_success(mock_recs, mock_config, mock_company, client):
    mock_company.return_value = "novibet"
    mock_config.return_value = {
        "recommendation": {
            "fields": {
                "event_id": {"type": "string"},
                "user_id": {"type": "int"}
            }
        }
    }
    mock_recs.return_value = [{"event_id": "e1", "user_id": 1}]

    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_fetch_dynamic_recommendations_missing_user_id(client):
    response = client.get("/recommendations")
    assert response.status_code == 400
    assert "error" in response.get_json()

#  /config [POST] 

@patch("app.main.save_company_config")
def test_set_config_success(mock_save, client):
    payload = {
        "recommender_type": "collaborative",
        "recommendation_schema": {
            "fields": ["user_id"],
            "labels": {"user_id": "ID"}
        }
    }
    headers = {"Casino-ID": "123"}
    response = client.post("/config", json=payload, headers=headers)
    assert response.status_code == 200
    assert "Configuration saved" in response.get_data(as_text=True)

def test_set_config_missing_header(client):
    payload = {"recommender_type": "any", "recommendation_schema": {}}
    response = client.post("/config", json=payload)
    assert response.status_code == 400
    assert "Casino-ID" in response.get_data(as_text=True)

def test_set_config_invalid_id(client):
    payload = {"recommender_type": "any", "recommendation_schema": {}}
    headers = {"Casino-ID": "abc"}
    response = client.post("/config", json=payload, headers=headers)
    assert response.status_code == 400
    assert "must be an integer" in response.get_data(as_text=True)

def test_set_config_invalid_payload(client):
    headers = {"Casino-ID": "123"}
    response = client.post("/config", json={}, headers=headers)
    assert response.status_code == 400

#  /config [GET] 

def test_get_static_config(client):
    response = client.get("/config")
    assert response.status_code == 200
    assert "user" in response.get_json()

