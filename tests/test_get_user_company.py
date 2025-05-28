from unittest.mock import patch, MagicMock
from app.db_bill import get_user_company
import pytest

@patch("app.db_bill.get_connection")
def test_get_user_company_returns_correct_company(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"company": "Stoiximan"}

    result = get_user_company(1)

    assert result == "Stoiximan"
    mock_cursor.execute.assert_called_once_with(
    "SELECT company FROM novibet_users WHERE user_id = %s", (1,)
)

@patch("app.db_bill.get_connection")
def test_get_user_company_returns_none_when_user_not_found(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    result = get_user_company(999)

    assert result is None

@patch("app.db_bill.get_connection")
def test_get_user_company_returns_none_if_company_missing(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {}  # no "company" key

    result = get_user_company(1)

    assert result is None

@patch("app.db_bill.get_connection")
def test_user_found_in_second_table(mock_conn):
    cursor_mock = MagicMock()
    mock_conn.return_value.cursor.return_value = cursor_mock

    # First table: None
    cursor_mock.fetchone.side_effect = [None, {"company": "Stoiximan"}]

    result = get_user_company(123)
    assert result == "Stoiximan"
    assert cursor_mock.execute.call_count == 2

@patch("app.db_bill.get_connection")
def test_get_user_company_db_connection_exception(mock_conn):
    mock_conn.side_effect = Exception("Database down")

    with pytest.raises(Exception, match="Database down"):
        get_user_company(1)


