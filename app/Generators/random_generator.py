import uuid
import random
from app.schemas import Recommendation
from app.recommender_registry import register

@register("random")
def generate_random_recommendations(user_id: int):
    recommendations = []
    for _ in range(3):
        recommendations.append(Recommendation(
            event_id=str(uuid.uuid4()),
            odds=round(random.uniform(1.5, 5.0), 2)
        ))
    return recommendations
