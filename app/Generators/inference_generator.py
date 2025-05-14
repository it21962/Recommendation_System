from app.schemas import Recommendation
from app.datastore import DataStore
from app.recommender_registry import register
from collections import Counter
from datetime import datetime, timedelta

datastore = DataStore()

@register("inference")
def inference_generator(user_id: int, sport: str = None):
    coupons = datastore.get_user_coupons(user_id)

    #Έλεγχος schema
    required_columns = {"sport", "league", "stake", "timestamp"}
    if not required_columns.issubset(coupons.columns):
        raise ValueError("Error: wrong schema")

    if coupons.empty:
        raise ValueError("No coupon data available for user.")

    # Φιλτράρισμα βάσει χρονου
    delta_t = timedelta(days=30)
    now = datetime.utcnow()
    recent = coupons[coupons["timestamp"] >= (now - delta_t)]

    if recent.empty:
        raise ValueError("No recent betting activity.")

    sport_league_pairs = list(zip(recent["sport"], recent["league"]))
    if not sport_league_pairs:
        raise ValueError("No sport/league data for recommendations.")

    top_pairs = Counter(sport_league_pairs).most_common(3)

    recommendations = []
    for (sport, league), _ in top_pairs:
        matched_events = datastore.get_events_by_sport_league(sport, league)
        if matched_events.empty:
            continue

        selected = matched_events.sample(1).iloc[0]
        home, away = selected["participants"].split(",")

        rec = Recommendation(
            event_id=selected["event_id"],
            home_team=home.strip(),
            away_team=away.strip(),
            odds_home=float(selected["odds_home"]),
            odds_away=float(selected["odds_away"]),
            stake=_get_average_stake(recent, sport, league),
            user_id=user_id
        )
        recommendations.append(rec)

    if not recommendations:
        raise ValueError("No matching events found for recommendations.")

    return recommendations

def _get_average_stake(recent_df, sport, league):
    filtered = recent_df[
        (recent_df["sport"] == sport) & (recent_df["league"] == league)
    ]
    if filtered.empty:
        raise ValueError("No stake data for selected sport/league.")
    return round(filtered["stake"].mean(), 2)
