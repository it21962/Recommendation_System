import pika
from datetime import datetime
from app.message_schemas.coupon import CouponCreated

coupon = CouponCreated(
    coupon_id="c123",
    user_id=33,
    timestamp=datetime.utcnow(),
    stake=20.0,
    sport="football",
    league="superleague",
    company="Novibet",
    selections="a1:1.80,a2:2.10"
)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="coupons_queue", durable=True)

channel.basic_publish(
    exchange="",
    routing_key="coupons_queue",
    body=coupon.json(),
    properties=pika.BasicProperties(delivery_mode=2)
)

print("Sent:", coupon.json())
connection.close()
