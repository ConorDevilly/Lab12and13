import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
import urllib2
 
# URL which returns a KEY which can be used to access SQS 
region = "us-east-1b"
 
#conn = boto.sqs.connect_to_region(region)
conn = boto.sqs.connect_to_region("us-east-1")
 
rs = conn.get_all_queues()
for q in rs:
	print q.id

