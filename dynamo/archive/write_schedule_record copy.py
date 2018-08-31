from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('BatchSchedules')

scheduleId = "daily-am-load"
item1 = {'scheduleId': scheduleId,"category": "this is a test category","jobList": {"stuff":"Nothing happens at all.",'morestuff': "some text", 'evenmore': 'stuff here'}}

scheduleId = "daily-pm-load"
item2 = { "scheduleId" : scheduleId,"category" : "big-data-schedules","scheduleName" : "Morning load and ETL workflow for big data","jobList": [{"jobName": "job1","jobDefinition": "arn:aws:batch:us-east-1:786247309603:job-definition/SampleJobDefinition-49e0468e4a867f5:1","jobQueue": "arn:aws:batch:us-east-1:786247309603:job-queue/SampleJobQueue-5da08f800c56cd4", "jobDependencies": [],"jobStatus": " ","jobId": " "},{ "jobName": "job2", "jobDefinition": "arn:aws:batch:us-east-1:786247309603:job-definition/SampleJobDefinition-49e0468e4a867f5:1","jobQueue": "arn:aws:batch:us-east-1:786247309603:job-queue/SampleJobQueue-5da08f800c56cd4", "jobDependencies": ["job1"], "jobStatus": " ", "jobId": " " } ], "scheduleStatus": " ", "wait_time": 60}

# test 1


response = table.put_item(
   Item={
        "scheduleId": "schedule A",
        "category": "test category",
        "jobList": {
            "stuff":"Nothing happens at all.",
            "morestuff": "some text"
        }
    }
)
print(json.dumps(response, indent=4, cls=DecimalEncoder))


# test2
response = table.put_item(
   Item= item1
)
print(json.dumps(response, indent=4, cls=DecimalEncoder))

# test 3
response = table.put_item(
   Item= item2
)
print(json.dumps(response, indent=4, cls=DecimalEncoder))

print("PutItem succeeded:")
