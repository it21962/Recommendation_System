from pydantic import BaseModel
from datetime import datetime

class EventPublished(BaseModel):
    event_type: str = "EventPublished"
    event_id: str
    sport: str
    league: str
    country: str
    begin_timestamp: datetime
    end_timestamp: datetime
    participants: str
    odds_home: float
    odds_away: float
