import pandas as pd
import pytest
from app.datastore import DataStore

@pytest.fixture
def datastore():
    users = pd.DataFrame({
        "user_id": [1, 2],
        "name": ["Alice", "Bob"]
    })

    events = pd.DataFrame({
        "event_id": ["e1", "e2"],
        "sport": ["football", "basket"],
        "league": ["superleague", "euroliga"],
        "participants": ["AEK,PAOK", "PAO,OLY"]
    })

    coupons = pd.DataFrame({
        "coupon_id": ["c1", "c2"],
        "user_id": [1, 2],
        "timestamp": ["2024-05-01", "2024-06-01"],
        "stake": [20.0, 25.0],
        "sport": ["football", "basket"],
        "league": ["superleague", "euroliga"],
        "company": ["novibet", "stoiximan"],
        "selections": ["some_match", "another_match"]
    })

    return DataStore(users, events, coupons)

def test_get_user_coupons(datastore):
    result = datastore.get_user_coupons(1)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result.iloc[0]["coupon_id"] == "c1"

def test_get_event_by_id_found(datastore):
    result = datastore.get_event_by_id("e1")
    assert result is not None
    assert result["participants"] == "AEK,PAOK"

def test_get_event_by_id_not_found(datastore):
    result = datastore.get_event_by_id("nonexistent")
    assert result is None

def test_get_all_users(datastore):
    result = datastore.get_all_users()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_get_all_events(datastore):
    result = datastore.get_all_events()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_get_events_by_sport_league(datastore):
    result = datastore.get_events_by_sport_league("football", "superleague")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result.iloc[0]["event_id"] == "e1"

def test_get_events_by_sport_league_invalid(datastore):
    result = datastore.get_events_by_sport_league(None, 123)
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_get_events_by_sport(datastore):
    result = datastore.get_events_by_sport("basket")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result.iloc[0]["event_id"] == "e2"
