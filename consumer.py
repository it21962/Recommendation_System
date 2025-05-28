
import pika
import json
from app.message_schemas.coupon import CouponCreated
from app.db_bill import insert_coupon

def callback(ch, method, properties, body):
    print("Received coupon message")
    try:
        data = json.loads(body)
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, str):
                    entry = json.loads(entry)
                coupon = CouponCreated(**entry)
                if insert_coupon(coupon):
                    print(f"Stored coupon (batch): {coupon.coupon_id}")
                else:
                    print(f"Coupon already exists: {coupon.coupon_id}")
        else:
            coupon = CouponCreated(**data)
            if insert_coupon(coupon):
                print(f"Stored coupon (single): {coupon.coupon_id}")
            else:
                print(f"Coupon already exists: {coupon.coupon_id}")
    except Exception as e:
        print("Error handling coupon message:", e)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="coupons_queue", durable=True)
channel.basic_consume(queue="coupons_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for coupons")
channel.start_consuming()
