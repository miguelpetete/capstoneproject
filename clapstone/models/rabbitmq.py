import pika


class RabbitMQ:
    def __init__(self, host="localhost"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def send_message(self, exchange, routing_key, body):
        self.channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=body
        )

    def consume_message(self, queue, callback):
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )

    def close(self):
        self.connection.close()
