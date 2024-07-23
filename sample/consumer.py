import pika

def callback(ch, method, properties, body):
    """
    Callback function to process incoming messages.

    Parameters:
    ch (pika.channel.Channel): The channel object
    method (pika.spec.Basic.Deliver): The delivery method
    properties (pika.spec.BasicProperties): The message properties
    body (bytes): The message body

    Example:
    >>> callback(ch, method, properties, b'Hello, world!')
    Received b'Hello, world!'
    """
    print("Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

def main():
    """
    Main function to set up RabbitMQ connection and start consuming messages.

    Example:
    >>> main()
    Waiting for messages. To exit press CTRL+C
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='chat_queue', durable=True)
    channel.basic_qos(prefetch_count=1)  # Fair dispatch
    channel.basic_consume(queue='chat_queue', on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()