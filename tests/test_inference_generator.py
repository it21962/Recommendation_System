import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app.Generators import inference_generator

from app.schemas import Recommendation

@patch("app.Generators.inference_generator.datastore")
def test_valid_input_returns_recommendations(mock_datastore):
    now = datetime.utcnow()
    coupons_df = pd.DataFrame([
        {
            "sport": "football",
            "league": "superleague",
            "stake": 50.0,
            "timestamp": now - timedelta(days=1)
        }
    ])
    events_df = pd.DataFrame([
        {
            "event_id": "event123",
            "participants": "AEK, PAOK",
            "odds_home": 2.1,
            "odds_away": 3.5
        }
    ])
    mock_datastore.get_user_coupons.return_value = coupons_df
    mock_datastore.get_events_by_sport_league.return_value = events_df

    recs = inference_generator(user_id=1)

    assert isinstance(recs, list)
    assert isinstance(recs[0], Recommendation)
    assert recs[0].home_team == "AEK"
    assert recs[0].away_team == "PAOK"
    assert recs[0].user_id == 1


@patch("app.Generators.inference_generator.datastore")
def test_empty_coupons_raises_value_error(mock_datastore):
    mock_datastore.get_user_coupons.return_value = pd.DataFrame(columns=["sport", "league", "stake", "timestamp"])
    with pytest.raises(ValueError, match="No coupon data available for user."):
        inference_generator(user_id=1)


@patch("app.Generators.inference_generator.datastore")
def test_missing_required_columns_raises_value_error(mock_datastore):
    df = pd.DataFrame([
        {"foo": 1, "bar": 2}
    ])
    mock_datastore.get_user_coupons.return_value = df
    with pytest.raises(ValueError, match="Error: wrong schema"):
        inference_generator(user_id=1)


@patch("app.Generators.inference_generator.datastore")
def test_no_recent_activity_raises_value_error(mock_datastore):
    old_date = datetime.utcnow() - timedelta(days=60)
    df = pd.DataFrame([
        {
            "sport": "football",
            "league": "la liga",
            "stake": 20.0,
            "timestamp": old_date
        }
    ])
    mock_datastore.get_user_coupons.return_value = df
    with pytest.raises(ValueError, match="No recent betting activity."):
        inference_generator(user_id=1)


@patch("app.Generators.inference_generator.datastore")
def test_no_matching_events_raises_value_error(mock_datastore):
    now = datetime.utcnow()
    coupons_df = pd.DataFrame([
        {
            "sport": "basketball",
            "league": "nba",
            "stake": 30.0,
            "timestamp": now
        }
    ])
    mock_datastore.get_user_coupons.return_value = coupons_df
    mock_datastore.get_events_by_sport_league.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="No matching events found for recommendations."):
        inference_generator(user_id=1)


@patch("app.Generators.inference_generator.datastore")
def test_no_stake_data_for_pair_raises_value_error(mock_datastore):
    now = datetime.utcnow()

    # Μόνο για "football", όχι για "basketball"
    coupons_df = pd.DataFrame([
        {
            "sport": "football",
            "league": "serie a",
            "stake": 100.0,
            "timestamp": now
        }
    ])

    # Event για άλλο sport/league χωρίς stake στο df
    events_df = pd.DataFrame([
        {
            "event_id": "E456",
            "participants": "Lakers, Celtics",
            "odds_home": 1.8,
            "odds_away": 2.5
        }
    ])

    # Προσποιούμαστε ότι το top_pair είναι αυτό χωρίς stake
    mock_datastore.get_user_coupons.return_value = coupons_df
    mock_datastore.get_events_by_sport_league.side_effect = lambda sport, league: (
        events_df if sport == "basketball" and league == "nba" else pd.DataFrame()
    )

    # Χειροκίνητο override για top_pairs
    with patch("app.Generators.inference_generator.Counter.most_common", return_value=[(("basketball", "nba"), 1)]):
        with pytest.raises(ValueError, match="No stake data for selected sport/league."):
            inference_generator(user_id=1)


