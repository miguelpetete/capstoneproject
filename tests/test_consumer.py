# import json
import pytest
import pika
from unittest import mock
from unittest.mock import Mock

from clapstone.models.rabbitmq import RabbitMQ


class TestConsumer:
    @pytest.mark.unit
    @mock.patch("clapstone.models.rabbitmq.pika.BlockingConnection", spec=pika.BlockingConnection)
    def test_consumer_is_connected_to_rabbitmq(self, connection_mock):
        channel_mock = Mock()
        connection_mock.return_value.channel.return_value = channel_mock

        subject = RabbitMQ()
        subject.consume_message("")
        channel_mock.basic_consume.assert_called()
        channel_mock.start_consuming.assert_called()


#    @pytest.mark.unit
#    @mock.patch("clapstone.models.rabbitmq.pika.BlockingConnection", spec=pika.BlockingConnection)
#    def test_a_new_message_is_processed(self, connection_mock):
#        connection_mock.return_value.channel.return_value.basic_consume.return_value  # pylint: disable= pointless-statement
#        subject = RabbitMQ()
#        subject._handle_message(  # pylint: disable= protected-access
#            ch="", method="", properties="", body=json.dumps({})
#        )
#        subject._handle_callback.assert_called()  # pylint: disable= protected-access
