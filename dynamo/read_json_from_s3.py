import boto3

data = {"HelloWorld": []}
s3 = boto3.resource('s3')
obj = s3.Object('batch-schedules','demo_schedule.json')
data = obj.get()['Body'].read()
print data