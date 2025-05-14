import pandas as pd
from pathlib import Path

class DataStore:
    def __init__(self, data_dir: str = "data"):
        base = Path(data_dir)

        self.users = pd.read_csv(base / "users.csv")

        self.events = pd.read_csv(base / "events.csv")
        self.coupons = pd.read_csv(
            base / "coupons.csv",
            parse_dates=["timestamp"],
            dtype={"user_id": int}
        )

    def get_user_coupons(self, user_id: int):
        self.coupons["user_id"] = self.coupons["user_id"].astype(int)
        return self.coupons[self.coupons["user_id"] == user_id]

    def get_event_by_id(self, event_id: str):
        match = self.events[self.events["event_id"] == event_id]
        return match.iloc[0].to_dict() if not match.empty else None

    def get_all_users(self):
        return self.users

    def get_all_events(self):
        return self.events

    def get_events_by_sport_league(self, sport, league):
        if not isinstance(sport, str) or not isinstance(league, str):
            return pd.DataFrame() 

        return self.events[
            (self.events["sport"].str.lower().str.strip() == sport) &
            (self.events["league"].str.lower().str.strip() == league)
    ]


    def get_events_by_sport(self, sport: str):
        sport = sport.strip().lower()
        return self.events[self.events["sport"] == sport]
