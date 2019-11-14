import pika

def declare_queue(channel, qname):
    action = "declare queue"
    try:
        channel.queue_declare(queue=qname, 
                            passive=False, 
                            durable=True
                            )
        response = {"queue": qname, "action": action, "status": "success"}
    
    except pika.exceptions.AMQPError as e:
        response = {"error": str(e), "action": action, "status": "failure"}
    
    return response

def delete_queue(channel, qname):
    action = "delete queue"
    try:
        channel.queue_delete(queue=qname)
        response = {"queue": qname, "action": action, "status": "success"}

    except (pika.exceptions.AMQPError, ValueError) as e:
        response = {"error": str(e), "action": action, "status": "failure"}
    
    return response

def list_queue(channel):
    # DB method: List out all spawned queues ever.
    return {}

def get_connection_status(connection):
    try:
        status = connection.is_open
        return {"Connection status": status}
    except Exception as e:
        return {"error": str(e)}

def purge_queue(channel, qname):
    action = "purge queue"
    try:
        channel.queue_purge(queue=qname)
        response = {"queue": qname, "action": action, "status": "success"}
    
    except (pika.exceptions.AMQPError, ValueError) as e:
        response = {"error": str(e), "action": action, "status": "failure"}

    return response

def push_message(channel, qname, message, exchange=None, routing_key=None):
    action = "publish message"
    try:
        channel.confirm_delivery()
        if exchange is None:
            exchange = ''
        if routing_key is None:
            routing_key = qname
        # Publish message
        channel.basic_publish(exchange='', 
                            routing_key=routing_key, 
                            body=message,
                            mandatory=True
                            )
        response = {"qname": qname, "action": action, "status": "success"}
    
    except (pika.exceptions.AMQPError, ValueError) as e:
        response = {"error": str(e), "action": action, "status": "failure"}

    return response

def retry_message(channel, qname, mid):
    # DB method: Push the messsage again in to rabbitmq.
    # Get message from database. 
    return {}

def switch_connection_status(connection):
    try:
        if connection.is_open:
            connection.close()
            message = "Closed the connection"
        return {"message": message}

    except (pika.exceptions.AMQPError, AttributeError) as e:
        return {"error": str(e)}