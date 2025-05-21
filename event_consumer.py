import pika, json
from app.message_schemas.event import EventPublished
from app.db_bill import insert_event

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        event = EventPublished(**data)
        insert_event(event)
        print("Stored event:", event.event_id)
    except Exception as e:
        print("Error:", e)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="events_queue", durable=True)
channel.basic_consume(queue="events_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for events")
channel.start_consuming()
