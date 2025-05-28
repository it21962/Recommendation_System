
import pika
import json
from app.message_schemas.user import UserRegistered
from app.db_bill import insert_user

def callback(ch, method, properties, body):
    print("Received user message")
    try:
        data = json.loads(body)
        if isinstance(data, list):
            for entry in data:
                user = UserRegistered(**entry)
                if insert_user(user):
                    print(f"Stored user (batch): {user.user_id}")
                else:
                    print(f"User already exists: {user.user_id}")
        else:
            user = UserRegistered(**data)
            if insert_user(user):
                print(f"Stored user (single): {user.user_id}")
            else:
                print(f"User already exists: {user.user_id}")
    except Exception as e:
        print("Error handling user message:", e)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="users_queue", durable=True)
channel.basic_consume(queue="users_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for users")
channel.start_consuming()
