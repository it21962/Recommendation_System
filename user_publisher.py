import pika
import json
from datetime import datetime
from app.message_schemas.user import UserRegistered

# Λίστα χρηστών προς αποστολή
users = [
    UserRegistered(
        event_type="UserRegistered",
        user_id=20,
        name="Bill hfee",
        birth_year=1997,
        country="GR",
        currency="EUR",
        gender="Male",
        registration_date=datetime.utcnow(),
        company="Novibet"
    ),
    UserRegistered(
        event_type="UserRegistered",
        user_id=21,
        name="Maria huojk",
        birth_year=1990,
        country="GR",
        currency="EUR",
        gender="Female",
        registration_date=datetime.utcnow(),
        company="Stoiximan"
    ),
]

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="users_queue", durable=True)

# Μετατροπή των users σε JSON κατάλληλο για RabbitMQ
message = json.dumps([user.model_dump(mode="json") for user in users])

channel.basic_publish(
    exchange="",
    routing_key="users_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print("Sent batch of users")
connection.close()
