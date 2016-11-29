#
import boto.sqs
import boto.sqs.queue
import argparse
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
sys.path.append('/data')
 
 
parser = argparse.ArgumentParser()
parser.add_argument("qname")
args = parser.parse_args()
 
conn = boto.sqs.connect_to_region("us-east-1")
 
try:
	q=conn.create_queue(args.qname)
	print args.qname, " queue has been created or already exists"
except:
	print "Could not create queue. possible too soon since deletion, wait 60 seconds"

