import unittest
from unittest.mock import MagicMock
from sample.consumer import callback

class TestConsumer(unittest.TestCase):

    def test_callback(self):
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_properties = MagicMock()
        body = b'Hello, World!'

        callback(mock_channel, mock_method, mock_properties, body)

        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

if __name__ == '__main__':
    unittest.main()