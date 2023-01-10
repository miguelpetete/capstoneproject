import pika


class MyProducer:
    def __init__(self, exchange_name, exchange_type):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type
        )

    def send_message(self, routing_key, message):
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key=routing_key, body=message
        )

    def close(self):
        self.connection.close()
