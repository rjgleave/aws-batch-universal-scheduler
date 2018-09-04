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

# This indicates where all of the batch job schedules are stored, for

# table contains job schedules. Each must be a json schedule record like this:

'''  Test file for Lambda
{    
  "scheduleId" : "daily-pm-load"
}
'''


'''   SAMPLE JOB SCHEDULE DOCUMENT - TO BE RETRIEVED FROM DYNAMODB
{    
    "scheduleId" : "daily-am-load",
    "category" : "big-data-schedules",
    "scheduleName" : "Morning load and ETL workflow for big data",
    "jobList": [
        {
            "jobName": "job1",
            "jobDefinition": "arn:aws:batch:us-east-1:786247309603:job-definition/SampleJobDefinition-49e0468e4a867f5:1",
            "jobQueue": "arn:aws:batch:us-east-1:786247309603:job-queue/SampleJobQueue-5da08f800c56cd4",
            "jobDependencies": [],
            "jobStatus": "",
            "jobId": ""
        },
        {
            "jobName": "job2",
            "jobDefinition": "arn:aws:batch:us-east-1:786247309603:job-definition/SampleJobDefinition-49e0468e4a867f5:1",
            "jobQueue": "arn:aws:batch:us-east-1:786247309603:job-queue/SampleJobQueue-5da08f800c56cd4",
            "jobDependencies": ["job1"],
            "jobStatus": "",
            "jobId": ""
        }
    ],
    "scheduleStatus": "",
    "wait_time": 60
}
'''


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

        #event['scheduleStatus'] = "SUCCEEDED"
        return item