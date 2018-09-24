import json
import boto3

import logging
# Initialize logger and set log level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading send_sns function...')
sns = boto3.client('sns')


def lambda_handler(event, context):
    # Log the received event
    #print("Received event: " + json.dumps(event, indent=2))
    email_message = "Hey man....  Your batch schedule: " + event['scheduleName'] + " [started: " + event['startDateTime'] + "] just finished.  Status: " + event['scheduleStatus']
    sms_message = "Job Complete. Status = " + event['scheduleStatus']
    sns_arn = event['scheduleSnsTopic']
    subject = 'Batch schedule ' + event['scheduleStatus']

    # Send message
    response = sns.publish(
        TargetArn=sns_arn,
        Message=json.dumps({'default': json.dumps(email_message),
                            'sms': json.dumps(sms_message),
                            'email': json.dumps(email_message)}),
        Subject=subject,
        MessageStructure='json'
    )

    logger.info(response)
    print('SNS function complete')
    print("Returned event: " + json.dumps(event, indent=2))
    return event