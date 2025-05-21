from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CouponCreated(BaseModel):
    event_type: str = "CouponCreated"
    coupon_id: str
    user_id: int
    timestamp: datetime
    stake: float
    sport: str
    league: str
    company: str
    selections: Optional[str] = None
