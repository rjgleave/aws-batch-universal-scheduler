Using AWS Batch as a Universal Job Scheduler
============================================

This solution utilizes AWS Batch to execute complex, multi-step job schedules across multiple platforms.   It takes advantage of the powerful AWS Batch job scheduling engine to handle complex job dependencies and automatically execute retries before failing.   It utilizes AWS Step Functions to start the schedule, monitor jobs and record results in AWS DynamoDb.

![Reference Architecture](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-universal-job-scheduler.png)

![](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-universal-job-scheduler-legend.png)

This example demonstrates the flexibility of using AWS Batch to act as both a worker actually perform work, or as an orchestrator, to direct other services to perform that work (e.g. AWS Glue, Lambda or EC2).   


What's Here
-----------

This repo includes:

1. README.md - this file
2. FOLDER: dynamo - this contains code to help build the sample schedule table in dynamoDB.  It includes:
    *   create_batch_schedule_table.py - this builds the schedule table
    *   write_schedule_record.py - this writes the S3 schedule record into dynamoDb
    *   sample_schedule.json - a sample schedule file which illustrates the structure
3. FOLDER: api-gateway - contains templates to help build and test the API REST interface
    *   test_message_start_machine.json - a sample document to illustrate the message used to trigger the schedule via the API.
4. FOLDER: state_machine  - components to build the state machine
    *   get_job_schedule.py - a lambda to retrieve the job schedule from dynamoDb
    *   poll_jobs.py - a lambda to poll the status of all submitted batch jobs.
    *   submit_jobs.py - lambda function to submit all batch jobs in the schedule. 
    *   JobStatusPollerStateMachine.json - definition of the state machine
    *   input-template.json - an input document that can be used to manually submit the state machine

Setup Instructions
------------------

Working Backwards, do the following:

1. Create the state machine. The easiest way is to use the online jumpstart (sample projects) which will build a basic state machine and all the AWS Batch infrastructure for you. Then you can modify it using the JobStatusPollerStateMachine definition provided in this repo.
![Step Functions Sample Projects](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/step-function-sample-projects.png))

2. Create all the lambdas needed for the state machine (see folder above)
Your state machine should look like this when you are done.
![State Machine](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-state-machine.png))

3. Create a sample schedule (see provided example in the folder above).  Make sure to update it with your batch job queue and other information.

![Sample Schedule](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/sample-schedule.png)

4. Create an S3 bucket to hold your job schedules.   Upload the schedule you created in the previous step above.

![S3 Bucket](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/s3-bucket.png)

5. Build DynamoDB table and load the S3 schedule into the table (use the programs provided in the folder above)

![DynamoDB](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/dynamodb-schedule-table.png)

6. Test your state machine manually, using the input-template.json document provided in the folder above.

![Input Document](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/sample-input-document.png)

7. Create the API which you will use to start the state machine by sending a message.  See the instruction link below if you need help doing that.    Use the provided test message in the folder above.

![API Gateway Message](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/sample-api-gateway-message.png)


__Additional Resources__

AWS documentation: Using API gateway to host a REST API to start a state machine
![Create API to start state machine](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-api-gateway.html)

AWS Step Functions.
https://aws.amazon.com/step-functions/