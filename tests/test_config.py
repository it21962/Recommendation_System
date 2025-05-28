import pytest
from app.main import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_config_success(client):
    response = client.get("/config")
    assert response.status_code == 200
    data = response.get_json()
    assert "user" in data
    assert "event" in data
    assert "recommendation" in data


@patch("app.main.save_company_config")
def test_post_config_valid_request(mock_save, client):
    payload = {
        "recommender_type": "inference",
        "recommendation_schema": {"fields": {"event_id": {"type": "string"}}}
    }
    headers = {"Casino-ID": "1"}

    response = client.post("/config", json=payload, headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "config" in data
    mock_save.assert_called_once()


def test_post_config_missing_casino_id(client):
    payload = {
        "recommender_type": "inference",
        "recommendation_schema": {"fields": {"event_id": {"type": "string"}}}
    }

    response = client.post("/config", json=payload)
    assert response.status_code == 400
    assert "Casino-ID header is required" in response.get_data(as_text=True)


def test_post_config_invalid_casino_id(client):
    headers = {"Casino-ID": "abc"}  # not integer
    payload = {
        "recommender_type": "inference",
        "recommendation_schema": {"fields": {"event_id": {"type": "string"}}}
    }

    response = client.post("/config", json=payload, headers=headers)
    assert response.status_code == 400
    assert "must be an integer" in response.get_data(as_text=True)


def test_post_config_invalid_body(client):
    headers = {"Casino-ID": "1"}
    payload = {}  # missing required fields

    response = client.post("/config", json=payload, headers=headers)
    assert response.status_code == 400
    assert "error" in response.get_json()


@patch("app.main.save_company_config")
def test_post_config_db_failure(mock_save, client):
    mock_save.side_effect = Exception("DB write error")
    headers = {"Casino-ID": "1"}
    payload = {
        "recommender_type": "inference",
        "recommendation_schema": {"fields": {"event_id": {"type": "string"}}}
    }

    response = client.post("/config", json=payload, headers=headers)
    assert response.status_code == 500
    assert "Failed to save config" in response.get_data(as_text=True)


from app.main import ConfigSchema
from datetime import datetime
from marshmallow import ValidationError

def test_config_schema_validates_and_adds_timestamp():
    schema = ConfigSchema()
    input_data = {
        "recommender_type": "inference",
        "recommendation_schema": {"fields": {"event_id": {"type": "string"}}}
    }
    result = schema.load(input_data)
    assert "timestamp" in result
    assert result["timestamp"].startswith(str(datetime.utcnow().year))


def test_config_schema_invalid_missing_fields():
    schema = ConfigSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"recommender_type": "inference"})  # missing recommendation_schema
    assert "recommendation_schema" in exc_info.value.messages


from app.db_bill import save_company_config
from unittest.mock import patch, MagicMock
import json


@patch("app.db_bill.get_connection")
def test_save_company_config_updates_existing(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # simulate row exists
    mock_conn.return_value.cursor.return_value = mock_cursor

    config_data = {"recommender_type": "inference"}
    save_company_config(1, config_data)

    config_str = json.dumps(config_data)
    mock_cursor.execute.assert_any_call("SELECT 1 FROM company_configs WHERE id = %s", (1,))
    mock_cursor.execute.assert_any_call(
        "UPDATE company_configs SET config = %s WHERE id = %s", (config_str, 1)
    )


@patch("app.db_bill.get_connection")
def test_save_company_config_raises_if_casino_id_missing(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # no matching row
    mock_conn.return_value.cursor.return_value = mock_cursor

    with pytest.raises(ValueError, match="Casino ID does not exist"):
        save_company_config(99, {"some": "config"})

from app.db_bill import get_display_config
from unittest.mock import patch, MagicMock
import json


@patch("app.db_bill.get_connection")
def test_get_display_config_returns_config(mock_conn):
    cursor_mock = MagicMock()
    mock_conn.return_value.cursor.return_value = cursor_mock

    fake_config = {"recommendation": {"fields": {"event_id": {"type": "string"}}}}
    cursor_mock.fetchone.return_value = {"config": json.dumps(fake_config)}

    result = get_display_config("novibet")

    assert result == fake_config
    cursor_mock.execute.assert_called_once_with(
        "SELECT config FROM company_configs WHERE company = %s", ("novibet",)
    )


@patch("app.db_bill.get_connection")
def test_get_display_config_returns_empty_when_none(mock_conn):
    cursor_mock = MagicMock()
    mock_conn.return_value.cursor.return_value = cursor_mock
    cursor_mock.fetchone.return_value = None

    result = get_display_config("missing_company")
    assert result == {}
