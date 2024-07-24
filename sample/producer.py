import os
from dotenv import load_dotenv
import pika

load_dotenv()

def send_message(queue_name, message):
    """
    Send a message to a RabbitMQ queue.

    Args:
        queue_name (str): The name of the queue to send the message to.
        message (str): The message to send.

    Example:
        >>> send_message('chat_queue', 'Hello, World!')

    This will send the message "Hello, World!" to the queue named "chat_queue".
    """
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2))  # make message persistent
    connection.close()

send_message('chat_queue', 'Hello, World!')