from flask import jsonify, request
from flask_api import status

from . import app, channel, connection
from .mq_actions import *
# setup rabbitmq connection

@app.route('/', methods=['GET', 'POST'])
def connectionMethod():
    # POST request
    if request.method == 'POST':
        response = switch_connection_status(connection)
    else:    
        response = get_connection_status(connection)
    return jsonify({"response": response})

@app.route('/queue', methods=['GET', 'POST'])
def queueAction():
    # POST request
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
def queueManage(qname):
    # DELETE request
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
def queuePurge(qname):
    try:
        response = purge_queue(channel, qname)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/queue/<string:qname>/message', methods=['POST'])
def messageAction(qname):
    message = request.form['message']
    try:
        messageResponse = push_message(channel, qname, message)
        # register message in the db
        return jsonify({"response": messageResponse})
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/queue/<string:qname>/message/<int:mid>', methods=['GET', 'POST'])
def messageHandler(qname, mid):
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
