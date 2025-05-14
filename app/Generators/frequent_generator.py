from app.schemas import CouponResponse
from app.datastore import DataStore
from app.recommender_registry import register
import random

datastore = DataStore()

@register("frequent")
def frequent_sport_generator(user_id: int, sport: str = None):
    if not sport:
        return _fallback_random(user_id)

    matched_events = datastore.get_events_by_sport(sport)
    if matched_events.empty:
        return _fallback_random(user_id)

    selected = matched_events.sample(1).iloc[0]
    home_team, away_team = selected["participants"].split(",")

    # Βρίσκει τα odds
    odds = datastore.get_odds_for_user_event(user_id, selected["event_id"])
    if odds is None:
        odds = round(random.uniform(1.5, 4.5), 2)

    # Βρίσκει το stake 
    coupons = datastore.get_user_coupons(user_id)
    stake = None
    for _, row in coupons.iterrows():
        for eid, _ in row["selections"]:
            if eid == selected["event_id"]:
                stake = row["stake"]
                break
        if stake:
            break

    if stake is None:
        stake = round(random.uniform(10, 50), 2)

    return [CouponResponse(
        event_id=selected["event_id"],
        home_team=home_team.strip(),
        away_team=away_team.strip(),
        odds=odds,
        stake=stake,
        user_id=user_id
    )]


def _fallback_random(user_id):
    return [CouponResponse(
        event_id=f"random-0",
        home_team="Team A",
        away_team="Team B",
        odds=round(random.uniform(1.5, 4.5), 2),
        stake=round(random.uniform(10, 50), 2),
        user_id=user_id
    )]
