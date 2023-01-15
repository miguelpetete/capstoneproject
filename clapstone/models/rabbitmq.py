# pylint: skip-file
import abc
import pika


class AbstractRabbitMQ(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_message(self, exchange, routing_key, body):
        pass

    @abc.abstractmethod
    def consume_message(self, queue, callback):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class RabbitMQ(AbstractRabbitMQ):
    def __init__(self, host="localhost"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self._handle_callback = None

    def send_message(self, exchange, routing_key, body):
        ret = self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
        return ret

    def consume_message(self, queue, callback=None):
        self._handle_callback = callback
        self.channel.basic_consume(queue=queue, on_message_callback=self._handle_message, auto_ack=True)
        self.channel.start_consuming()

    def _handle_message(self, ch, method, properties, body):
        if self._handle_callback:
            self._handle_callback(ch, method, properties, body)

    def close(self):
        self.channel.stop_consuming()
        self.connection.close()
