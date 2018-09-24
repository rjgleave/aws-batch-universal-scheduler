console.log('Loading function');
const aws = require('aws-sdk');

exports.lambda_handler = (event, context, callback) => {
    const sns = new aws.SNS();
    console.log(`Sending message to SNS topic ${event.ScheduleSnsTopic}`);
    const messageInfo = {
        Message: event.ScheduleMessage,
        TopicArn: event.ScheduleSnsTopic       
    };
    sns.publish(messageInfo, (err, data) => {
        if (err) {
            console.error(err.message);
            callback(err.message, event);
            return;
        }
        console.log(data);
        callback(err, event);
    });
};