import pika, json
from app.message_schemas.user import UserRegistered
from app.db_bill import insert_user

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        user = UserRegistered(**data)
        insert_user(user)
        print("Stored user:", user.user_id)
    except Exception as e:
        print("Error:", e)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="users_queue", durable=True)
channel.basic_consume(queue="users_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for users")
channel.start_consuming()
