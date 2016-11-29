
import boto.sqs

import boto.sqs.queue

import argparse

from boto.sqs.message import Message

from boto.sqs.connection import SQSConnection

from boto.exception import SQSError

parser = argparse.ArgumentParser()

parser.add_argument("qname")

args = parser.parse_args()



conn = boto.sqs.connect_to_region("us-east-1")



try:

	q=conn.get_queue(args.qname)

except:

	print "Failed to find queue ",args.qname

try:

	conn.delete_queue(q,True)

	print args.qname, " queue has been deleted"

except:

	print "Could not delete the queue, or it does not exist"

