import os
import logging
from dotenv import load_dotenv
import pika

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def callback(ch, method, properties, body):
    """
    Callback function to process incoming messages.

    Parameters:
    ch (pika.channel.Channel): The channel object
    method (pika.spec.Basic.Deliver): The delivery method
    properties (pika.spec.BasicProperties): The message properties
    body (bytes): The message body
    """
    pod_name = os.getenv('HOSTNAME')
    message = body.decode('utf-8')
    logging.info(f"Pod {pod_name} received message: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

def main():
    """
    Main function to set up RabbitMQ connection and start consuming messages.
    """
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
    rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection_params = pika.ConnectionParameters(rabbitmq_host, credentials=credentials)

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='chat_queue', durable=True)
    channel.basic_qos(prefetch_count=1)  # Fair dispatch
    channel.basic_consume(queue='chat_queue', on_message_callback=callback)
    logging.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()