from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
import urllib2
import json
	
app = Flask(__name__)

# AWS Region
region = "us-east-1"

@app.route('/queues', methods=['GET'])
def listAllQueues():
	conn = boto.sqs.connect_to_region(region)
	rs = conn.get_all_queues()
	queues = []
	for q in rs:
		queues.append(q.name)
	return jsonify({'queues' : queues})

@app.route('/queues', methods=['POST'])
def createQueue():
	if not request.json or not 'name' in request.json:
		abort(400)
	qname = request.json.get('name')
	conn = boto.sqs.connect_to_region(region)
	print(qname)
	try:
		q = conn.create_queue(qname)
		return jsonify({'queue' : q.name}), 201
	except:
		abort(400)
		return jsonify({'ERROR' : 'Q could not be created'})

@app.route('/queues/<qid>', methods=['DELETE'])
def deleteQueue(qid):
	conn = boto.sqs.connect_to_region(region)

	try:
		q = conn.get_queue(qid)
	except:
		return jsonify({'ERROR' : "Failed to find queue"}), 400
	try:
		conn.delete_queue(q, True)
		return jsonify({'result': True})
	except:
		return jsonify({'ERROR' : "Could not delete the queue, or it does not exist"}), 404

@app.route('/queues/<qid>/msgs', methods=['GET'])
def getMsg(qid):
	conn = boto.sqs.connect_to_region(region)
	q = conn.get_queue(qid)

	try:
		m = Message()
		m = q.read(60)
		str1 = m.get_body()
		return jsonify({'message' : str1}), 200
	except:
		return jsonify({'ERROR' : "Could not read message or queue does not exist"}), 404

@app.route('/queues/<qid>/msgs', methods=['POST'])
def postMsg(qid):
	if not request.json or not 'content' in request.json:
		abort(400)
	content = request.json.get('content')

	conn = boto.sqs.connect_to_region(region)
	q = conn.get_queue(qid)

	try:
		m = Message()
		m.set_body(content)
		q.write(m)
		return jsonify({'result' : True}), 200
	except:
		return jsonify({'ERROR' : "Could not write message to queue or queue does not exist"}), 404

@app.route('/queues/<qid>/msgs/count', methods=['GET'])
def getMsgCount(qid):
	conn = boto.sqs.connect_to_region(region)
	q = conn.get_queue(qid)

	try:
		counter = q.count()
		return jsonify({'count' : counter}), 200
	except:
		return jsonify({'ERROR' : 'Could not count message or queue does not exist'}), 404
	
@app.route('/queues/<qid>/msgs', methods=['DELETE'])
def consumeMsg(qid):
	conn = boto.sqs.connect_to_region(region)
	q = conn.get_queue(qid)
	try:
		m = Message()
		m = q.read(60)
		str1 = m.get_body()
	except:
		return jsonify({'ERROR' : "Could not read message or queue does not exist"}), 404

	try:
		q.delete_message(m)
		return jsonify({'message' : str1}), 200
	except:
		return jsonify({'ERROR' : "Could not delete message or queue does not exist"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True) 
