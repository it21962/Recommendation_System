import pika
from datetime import datetime
from app.message_schemas.user import UserRegistered

user = UserRegistered(
    event_type="UserRegistered",
    user_id=33,
    name="Bill N",
    birth_year=1990,
    country="GR",
    currency="EUR",
    gender="Male",
    registration_date=datetime.utcnow(),
    company="Novibet"
)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="users_queue", durable=True)

channel.basic_publish(
    exchange="",
    routing_key="users_queue",
    body=user.model_dump_json(),
    properties=pika.BasicProperties(delivery_mode=2)
)

print("User sent:", user.model_dump_json())
connection.close()
