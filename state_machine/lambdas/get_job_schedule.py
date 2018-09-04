from __future__ import print_function

import json
import urllib
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


print('Loading get_job_schedule function')

# NOTE: YOU MUST SET UP THE REGION VARIABLE IN THE LAMBDA!
# Import Environment Variables for Lambda configuration
REGION = os.environ['AWS_REGION']

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table('BatchSchedules')


def lambda_handler(event, context):
    # Log the received event
    
    print("Received event: " + json.dumps(event, indent=2))

    # Get the name of the category and batch schedule from the state machine input document
    schedule_id = event['scheduleId']
    
    try:
        response = table.get_item(
            Key={
                'scheduleId': schedule_id
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))

        return item