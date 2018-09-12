from __future__ import print_function

import json
import urllib
import boto3
import os
import decimal
from datetime import datetime
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


print('Loading update_schedule_history function')

# NOTE: YOU MUST SET UP THE REGION VARIABLE IN THE LAMBDA!
# Import Environment Variables for Lambda configuration
REGION = os.environ['AWS_REGION']

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table('BatchScheduleHistory')


def lambda_handler(event, context):
    # Log the received event
    
    #print("Received event: " + json.dumps(event, indent=2))
    wt = event['wait_time']
    if type(wt) == float:
        print(type(wt))
        wt2 = format(wt, ".15g")
        event['wait_time'] = format(wt, ".15g")
        print(type(wt2))

    # update the timestamps
    event['lastDateTime'] = datetime.utcnow().isoformat()
    if not 'startDateTime' in event:
        event['startDateTime'] = event['lastDateTime']
    
    try:
        response = table.put_item(
        Item= event
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("history update succeeded:")
        return event