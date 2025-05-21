from pydantic import BaseModel
from datetime import datetime

class UserRegistered(BaseModel):
    event_type: str = "UserRegistered"
    user_id: int
    name: str
    birth_year: int
    country: str
    currency: str
    gender: str
    registration_date: datetime
    company: str
