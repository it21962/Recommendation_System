
import pika
import json
from app.message_schemas.event import EventPublished
from app.db_bill import insert_event

def callback(ch, method, properties, body):
    print("Received event message")
    try:
        data = json.loads(body)
        if isinstance(data, list):
            for entry in data:
                event = EventPublished(**entry)
                if insert_event(event):
                    print(f"Stored event (batch): {event.event_id}")
                else:
                    print(f"Event already exists: {event.event_id}")
        else:
            event = EventPublished(**data)
            if insert_event(event):
                print(f"Stored event (single): {event.event_id}")
            else:
                print(f"Event already exists: {event.event_id}")
    except Exception as e:
        print("Error handling event:", e)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="events_queue", durable=True)
channel.basic_consume(queue="events_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for events")
channel.start_consuming()
