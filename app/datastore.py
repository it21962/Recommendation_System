import pandas as pd

class DataStore:
    def __init__(self, users_df=None, events_df=None, coupons_df=None):
        self.users = users_df if users_df is not None else pd.DataFrame()
        self.events = events_df if events_df is not None else pd.DataFrame()
        self.coupons = coupons_df if coupons_df is not None else pd.DataFrame()

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

        sport = sport.lower().strip()
        league = league.lower().strip()

        return self.events[
            (self.events["sport"].str.lower().str.strip() == sport) &
            (self.events["league"].str.lower().str.strip() == league)
        ]

    def get_events_by_sport(self, sport: str):
        sport = sport.strip().lower()
        return self.events[self.events["sport"].str.lower().str.strip() == sport]
