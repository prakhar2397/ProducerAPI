from flask import Flask
import pika

# Settings
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = '/'
RABBITMQ_HEARTBEAT = 600
RABBITMQ_CONNECTION_TIMEOUT = 300

# Setup rabbitmq connection
def connect_rabbit():
    credentials = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VHOST,
        heartbeat=RABBITMQ_HEARTBEAT,
        blocked_connection_timeout=RABBITMQ_CONNECTION_TIMEOUT
    )
    connection = pika.BlockingConnection(credentials)
    channel = connection.channel()
    return connection, channel
# Setup db connection

app = Flask(__name__)
connection, channel = connect_rabbit()

from . import views
