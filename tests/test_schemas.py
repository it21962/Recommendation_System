from app.schemas import Recommendation

def test_recommendation_dict_method():
    rec = Recommendation(
        event_id="e1",
        home_team="AEK",
        away_team="PAOK",
        odds_home=1.9,
        odds_away=2.1,
        stake=20.0,
        user_id=1
    )

    result = rec.dict()
    assert isinstance(result, dict)
    assert result["event_id"] == "e1"
    assert result["stake"] == 20.0
