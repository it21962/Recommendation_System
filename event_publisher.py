import pika
import json
from datetime import datetime
from app.message_schemas.event import EventPublished

events = [
    EventPublished(
        event_type="EventPublished",
        event_id="e4",
        sport="volleyball",
        league="international",
        country="Italy",
        begin_timestamp=datetime(2025, 6, 10, 18, 0),
        end_timestamp=datetime(2025, 6, 10, 20, 0),
        participants="ITA,BRA",
        odds_home=2.10,
        odds_away=1.85
    ),
    EventPublished(
        event_type="EventPublished",
        event_id="e5",
        sport="football",
        league="euros",
        country="Germany",
        begin_timestamp=datetime(2025, 6, 15, 21, 0),
        end_timestamp=datetime(2025, 6, 15, 23, 0),
        participants="GER,FRA",
        odds_home=2.40,
        odds_away=2.00
    ),
]

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="events_queue", durable=True)

message = json.dumps([event.model_dump(mode="json") for event in events])

channel.basic_publish(
    exchange="",
    routing_key="events_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print("Sent batch of events")
connection.close()
