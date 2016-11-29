
import boto.sqs

import boto.sqs.queue

import argparse

from boto.sqs.message import Message

from boto.sqs.connection import SQSConnection

from boto.exception import SQSError


parser = argparse.ArgumentParser()

parser.add_argument("qname")
parser.add_argument("message")

args = parser.parse_args()



conn = boto.sqs.connect_to_region("us-east-1")
m = Message()

try:

	q=conn.get_queue(args.qname)

except:

	print "Failed to find queue ",args.qname

try:
	print args.message 
	m.set_body(args.message)
        q.write(m)
	print args.message, " The message has been posted"

except:

	print "Could not write the message to queue, or queue does not exist"

