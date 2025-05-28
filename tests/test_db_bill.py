import pytest
from unittest.mock import patch, MagicMock
from app.db_bill import (
    insert_event, insert_user, insert_coupon,
    get_dynamic_recommendations, save_company_config
)
import json

# Dummy κλάσεις
class DummyEvent:
    event_id = "e123"
    sport = "football"
    league = "superleague"
    country = "GR"
    begin_timestamp = "2025-06-01"
    end_timestamp = "2025-06-01"
    participants = "AEK,PAOK"
    odds_home = 1.9
    odds_away = 2.1

class DummyUser:
    user_id = 42
    name = "Basil"
    birth_year = 1990
    country = "GR"
    currency = "EUR"
    gender = "M"
    registration_date = "2024-01-01"
    company = "Stoiximan"

class DummyCoupon:
    coupon_id = "coup001"
    user_id = 1
    timestamp = "2024-05-01"
    stake = 20
    sport = "football"
    league = "superleague"
    company = "novibet"
    selections = "match1"

@patch("app.db_bill.get_connection")
def test_insert_event_when_not_exists(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    mock_conn.return_value.cursor.return_value = cursor
    assert insert_event(DummyEvent()) is True


@patch("app.db_bill.get_connection")
def test_insert_event_already_exists(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = (1,)
    mock_conn.return_value.cursor.return_value = cursor
    assert insert_event(DummyEvent()) is False

@patch("app.db_bill.get_connection")
def test_insert_user_when_not_exists(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    mock_conn.return_value.cursor.return_value = cursor
    assert insert_user(DummyUser()) is True


@patch("app.db_bill.get_connection")
def test_insert_user_already_exists(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = (1,)
    mock_conn.return_value.cursor.return_value = cursor
    assert insert_user(DummyUser()) is False

@patch("app.db_bill.get_connection")
def test_insert_coupon_when_not_exists(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    mock_conn.return_value.cursor.return_value = cursor
    assert insert_coupon(DummyCoupon()) is True


@patch("app.db_bill.get_connection")
def test_insert_coupon_already_exists(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = (1,)
    mock_conn.return_value.cursor.return_value = cursor
    assert insert_coupon(DummyCoupon()) is False

@patch("app.db_bill.get_connection")
def test_get_dynamic_recommendations_success(mock_conn):
    cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = cursor

    # 1η fetch: interests, 2η fetch: matched events
    cursor.fetchall.side_effect = [
        [{"sport": "football", "league": "superleague"}],
        [{
            "event_id": "e123",
            "participants": "AEK,PAOK",
            "odds_home": 1.9,
            "odds_away": 2.1,
            "begin_timestamp": "2025-01-01",
            "end_timestamp": "2025-01-01"
        }]
    ]

    recs = get_dynamic_recommendations(1)
    assert isinstance(recs, list)
    assert recs[0]["home_team"] == "AEK"
    assert recs[0]["stake"] == 20.0


from app.db_bill import save_company_config

@patch("app.db_bill.get_connection")
def test_save_company_config_invalid_id(mock_conn):
    cursor = MagicMock()
    cursor.fetchone.return_value = None  # <- δεν υπάρχει το id
    mock_conn.return_value.cursor.return_value = cursor

    with pytest.raises(ValueError, match="Casino ID does not exist in company_configs"):
        save_company_config(999, {"some": "config"})

@patch("app.db_bill.get_connection")
def test_get_dynamic_recommendations_no_interests(mock_conn):
    cursor = MagicMock()
    cursor.fetchall.side_effect = [[]]  # <== 1η κλήση returns empty
    mock_conn.return_value.cursor.return_value = cursor

    result = get_dynamic_recommendations(user_id=99)
    assert result == []
