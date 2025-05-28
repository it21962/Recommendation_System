import pika
import json
from datetime import datetime
from app.message_schemas.coupon import CouponCreated

# Παράδειγμα: πολλά κουπόνια
coupons = [
    CouponCreated(
        coupon_id="c13",
        user_id=13,
        timestamp=datetime.utcnow(),
        stake=30.0,
        sport="basketball",
        league="euroleague",
        company="Stoiximan",
        selections="a2:1.95"
    ),
    CouponCreated(
        coupon_id="c10",
        user_id=10,
        timestamp=datetime.utcnow(),
        stake=50.0,
        sport="football",
        league="superleague",
        company="Stoiximan",
        selections="a2:2.40"
    ),
]

message = json.dumps([coupon.model_dump() for coupon in coupons], default=str)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="coupons_queue", durable=True)

channel.basic_publish(
    exchange="",
    routing_key="coupons_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print("Sent batch of coupons")
connection.close()
