Using AWS Batch as a Universal Job Scheduler
============================================

This solution utilizes AWS Batch to execute complex, multi-step job schedules across multiple platforms.   It takes advantage of the powerful AWS Batch job scheduling engine to handle complex job dependencies and automatically execute retries.   It utilizes AWS Step Functions to initiate schedules, monitor and record results in AWS DynamoDb.

![Reference Architecture](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-universal-job-scheduler.png)

![](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-universal-job-scheduler-legend.png)

This architecture provides the flexibility of using AWS Batch to act as a worker and actually perform work, or to direct other services to perform that work (e.g. AWS Glue, Lambda or EC2).   


What's Here
-----------

This repo includes:

1. README.md - this file
2. FOLDER: dynamo - this contains code to help build the sample 
transaction table in dynamoDB.  It includes:
    *   schema.json - an example of the dynamoDB schema data structure
    *   read_dynamo_stream.py - the lambda program which reads the dynamodb streams
    *   test_streams.json - a sample stream file for testing the lambda above.
3. FOLDER: api-gateway - contains templates to help build and test the API REST interface
    *   api_gateway_mapping_template.json - this is the mapping document used to create the proxy api for the state machine service.
    *   test_message.json - copy the json document and use to test the API.
4. FOLDER: state_machine  - components to build the state machine
    *   JobStatusPoller.py - a lambda to poll the status of batch jobs.
    *    SubmitJobFunction.py - lambda function to submit a batch job. 
    *   JobStatusPollerStateMachine.json - definition of the state machine
    *   input-template.json - the document used to submit the state machine

Setup Instructions
------------------

Working Backwards, do the following:

1. Create the state machine.  The easiest way to do this is to use the online jumpstart which will build it for you.  See instructions here:
![Reference Architecture](https://github.com/rjgleave/aws-batch-api-submitter/blob/master/assets/step-function-sample-projects.png)

2. Use the schema to build DynamoDB table.   Make sure you turn on streaming.
3. Install the lambda to read the dynamodb stream.   You will need to modify it to pass in the input document and ARN of the state machine.    You can test it using the test_streams.json document.
4. Create the API.  Use the provided mapping document.



__Additional Resources__

Blog: Using Amazon API Gateway as a proxy for DynamoDB
https://aws.amazon.com/blogs/compute/using-amazon-api-gateway-as-a-proxy-for-dynamodb/

SWS Step Functions
https://aws.amazon.com/step-functions/