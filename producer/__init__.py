from flask import Flask
import pika

# Settings
class RabbitMQConfig:
    def __init__(self):
        self.RABBITMQ_HOST = 'localhost'
        self.RABBITMQ_PORT = 5672
        self.RABBITMQ_VHOST = '/'
        self.RABBITMQ_HEARTBEAT = 10
        self.RABBITMQ_CONNECTION_TIMEOUT = 5

# Setup rabbitmq connection
def connect_rabbit():
    config = RabbitMQConfig()
    credentials = pika.ConnectionParameters(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        virtual_host=config.RABBITMQ_VHOST,
        heartbeat=config.RABBITMQ_HEARTBEAT,
        blocked_connection_timeout=config.RABBITMQ_CONNECTION_TIMEOUT
    )
    connection = pika.BlockingConnection(credentials)
    channel = connection.channel()
    return connection, channel
# Setup db connection

app = Flask(__name__)
connection, channel = connect_rabbit()

# Allow reconnection
def isConnected(func):
    def inner(*args, **kwargs):
        global connection
        global channel
        try:
            connection.process_data_events()
            print("Connection exists.")
        except (pika.exceptions.ConnectionClosed, pika.exceptions.StreamLostError) as e:
            print("Connection closed. Reconnecting....")
            connection, channel = connect_rabbit()
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner

from . import views