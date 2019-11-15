from flask import jsonify, request
from flask_api import status

from . import app, isConnected
from .mq_actions import *
# setup rabbitmq connection

@app.route('/', methods=['GET', 'POST'])
@isConnected
def connectionMethod():
    # POST request
    from . import channel, connection
    if request.method == 'POST':
        response = switch_connection_status(connection)
    else:    
        response = get_connection_status(connection)
    return jsonify({"response": response})

@app.route('/queue', methods=['GET', 'POST'])
@isConnected
def queueAction():
    # POST request
    from . import channel, connection
    if request.method == 'POST':
        try:
            qname = request.form['qname']
            response = declare_queue(channel, qname)
            # store queue data in database
            return jsonify({"response": response})

        except Exception as e:
            return jsonify({"error": str(e)})
    
    try:
        response = list_queue(channel)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/queue/<string:qname>', methods=['GET', 'DELETE'])
@isConnected
def queueManage(qname):
    # DELETE request
    from . import channel, connection
    if request.method == 'DELETE':
        try:
            response = delete_queue(channel, qname)
            # update database; return response
            return jsonify({"response": response})
        
        except Exception as e:
            return jsonify({"error": str(e)})
    
    try:
        response = list_message(channel, qname)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/queue/<string:qname>/purge', methods=['POST'])
@isConnected
def queuePurge(qname):
    from . import channel, connection
    try:
        response = purge_queue(channel, qname)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/queue/<string:qname>/message', methods=['POST'])
@isConnected
def messageAction(qname):
    from . import channel, connection
    message = request.form['message']
    try:
        messageResponse = push_message(channel, qname, message)
        # register message in the db
        return jsonify({"response": messageResponse})
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/queue/<string:qname>/message/<int:mid>', methods=['GET', 'POST'])
@isConnected
def messageHandler(qname, mid):
    from . import channel, connection
    try:
        res_status = status.HTTP_202_ACCEPTED
        if request.method == 'POST':
            messageResponse = retry_message(channel, qname, mid)
            # update in database
        else:
            messageResponse = get_message(channel, qname, mid)
            res_status = status.HTTP_200_OK
        
        return jsonify({"response": messageResponse})

    except Exception as e:
        return jsonify({"error": str(e)})
