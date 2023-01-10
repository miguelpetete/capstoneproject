"""Abstract Class for the consumer of the queue of RabbitMQ"""
from abc import ABC, abstractmethod
import pika


class MyConsumer(ABC):
    """Initializer of the class consumer"""

    def __init__(self, queue_name, exchange_name, exchange_type):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue_name)
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type
        )
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)

    def start(self):
        """Start the connection with the rabbitmq"""
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.function_to_consume,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def stop(self):
        """Stop the connection to the rabbitmq"""
        self.channel.stop_consuming()
        self.connection.close()

    @abstractmethod
    def function_to_consume(self):
        """Abstract class that is different in every consumer"""
