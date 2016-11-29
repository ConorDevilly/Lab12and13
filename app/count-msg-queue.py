#
import boto.sqs
import boto.sqs.queue
import argparse
from boto.sqs.attributes import Attributes
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError



parser = argparse.ArgumentParser()
parser.add_argument("qname")
args = parser.parse_args()

conn = boto.sqs.connect_to_region("us-east-1")
q = conn.get_queue(args.qname)

try:
	counter = q.count()
	print "Messages in Queue = ", counter
except:
	print "Could not read message"

