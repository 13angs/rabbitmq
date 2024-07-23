import unittest
from unittest.mock import patch, MagicMock

import pika
from sample.producer import send_message

class TestProducer(unittest.TestCase):

    @patch('pika.BlockingConnection')
    def test_send_message(self, mock_blocking_connection):
        mock_channel = MagicMock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel
        
        send_message('test_queue', 'Hello, World!')
        
        mock_blocking_connection.assert_called_once_with(pika.ConnectionParameters('localhost'))
        mock_channel.queue_declare.assert_called_once_with(queue='test_queue', durable=True)
        mock_channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='test_queue',
            body='Hello, World!',
            properties=pika.BasicProperties(delivery_mode=2)
        )
        mock_blocking_connection.return_value.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()