import pika
from datetime import datetime
from app.message_schemas.event import EventPublished

event = EventPublished(
    event_type="EventPublished",
    event_id="e100",
    sport="football",
    league="superleague",
    country="Greece",
    begin_timestamp=datetime(2025, 6, 1, 19, 0),
    end_timestamp=datetime(2025, 6, 1, 21, 0),
    participants="PAOK,AEK",
    odds_home=2.10,
    odds_away=2.90
)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="events_queue", durable=True)

channel.basic_publish(
    exchange="",
    routing_key="events_queue",
    body=event.model_dump_json(),
    properties=pika.BasicProperties(delivery_mode=2)
)

print("Event sent:", event.model_dump_json())
connection.close()
