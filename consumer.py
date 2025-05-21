import pika
import json
from app.message_schemas.coupon import CouponCreated
from app.db_bill import insert_coupon

def callback(ch, method, properties, body):
    print("Received message:")
    try:
        data = json.loads(body)
        coupon = CouponCreated(**data)
        insert_coupon(coupon)
        print("Stored in DB:", coupon.coupon_id)

        from app.Generators import get_generator
        from app.db_bill import insert_recommendation

        generator = get_generator("inference")
        recommendations = generator(coupon.user_id)

        for rec in recommendations:
            insert_recommendation(rec)

        print(f"Generated {len(recommendations)} recommendations for user {coupon.user_id}")

    except Exception as e:
        print("Error handling message:", e)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="coupons_queue", durable=True)
channel.basic_consume(queue="coupons_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
