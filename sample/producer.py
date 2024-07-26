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
    """
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
    rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection_params = pika.ConnectionParameters(rabbitmq_host, credentials=credentials)
    
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2))  # make message persistent
    connection.close()

send_message('chat_queue', 'Hello, World!')