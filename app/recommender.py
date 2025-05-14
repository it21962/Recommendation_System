from .schemas import Recommendation
import random
import uuid

def generate_mock_recommendations(user_id: int) -> list[Recommendation]:
    return [
        Recommendation(
            event_id=str(uuid.uuid4()),
            odds=round(random.uniform(1.5, 5.0), 2)
        )
        for _ in range(3)
    ]
