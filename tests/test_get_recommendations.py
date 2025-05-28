import pytest
from unittest.mock import patch, MagicMock
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("app.main.get_user_company")
@patch("app.main.get_display_config")
@patch("app.main.get_dynamic_recommendations")
def test_get_recommendations_success(mock_recs, mock_config, mock_company, client):
    mock_company.return_value = "novibet"
    mock_config.return_value = {
        "recommendation": {
            "fields": {
                "event_id": {"type": "string"},
                "user_id": {"type": "int"},
                "home_team": {"type": "string", "source_field": "home_team"}
            }
        }
    }
    mock_recs.return_value = [
        {"event_id": "E1", "user_id": 1, "home_team": "AEK"}
    ]

    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["home_team"] == "AEK"


def test_get_recommendations_missing_user_id(client):
    response = client.get("/recommendations")
    assert response.status_code == 400
    assert "error" in response.get_json()


@patch("app.main.get_user_company")
def test_get_recommendations_user_not_found(mock_company, client):
    mock_company.return_value = None
    response = client.get("/recommendations?user_id=999")
    assert response.status_code == 404
    assert "User not found" in response.get_data(as_text=True)


@patch("app.main.get_user_company")
@patch("app.main.get_display_config")
def test_get_recommendations_invalid_config(mock_config, mock_company, client):
    mock_company.return_value = "novibet"
    mock_config.side_effect = Exception("DB error")
    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 500
    assert "DB error" in response.get_data(as_text=True)


@patch("app.main.get_user_company")
@patch("app.main.get_display_config")
@patch("app.main.get_dynamic_recommendations")
def test_get_recommendations_with_empty_schema(mock_recs, mock_config, mock_company, client):
    mock_company.return_value = "novibet"
    mock_config.return_value = {}  # No "recommendation" key
    mock_recs.return_value = [{"event_id": "E1", "user_id": 1, "home_team": "AEK"}]

    response = client.get("/recommendations?user_id=1")

    assert response.status_code == 200
    # dump on schema with no fields gives [{}] per item
    assert response.get_json() == [{}]




