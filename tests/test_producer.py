from unittest import mock
import pika
import pytest

from clapstone.models.rabbitmq import RabbitMQ


class TestProducer:
    @pytest.mark.unit
    @mock.patch("clapstone.models.rabbitmq.pika.BlockingConnection", spec=pika.BlockingConnection)
    def test_send_message(self, connection_mock):
        connection_mock.return_value.channel.return_value.basic_publish.return_value = True
        subject = RabbitMQ()
        body = {}
        assert subject.send_message("", "routing_key", body) is True
