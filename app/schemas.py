from pydantic import BaseModel

class UserRequest(BaseModel):
    user_id: int
    algorithm: str = "inference"
    sport: str | None = None


class Recommendation(BaseModel):
    event_id: str
    home_team: str
    away_team: str
    odds_home: float
    odds_away: float
    stake: float
    user_id: int

    def dict(self, **kwargs):
        return {
            "event_id": self.event_id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "odds_home": self.odds_home,
            "odds_away": self.odds_away,
            "stake": self.stake,
            "user_id": self.user_id
        }



class CouponResponse(BaseModel):
    event_id: str
    home_team: str
    away_team: str
    odds: float
    stake: float
    user_id: int
