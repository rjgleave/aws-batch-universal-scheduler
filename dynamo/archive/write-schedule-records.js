require 'aws-sdk-dynamodb'  
require 'json'

# Create dynamodb client in us-east-1 region
dynamodb = Aws::DynamoDB::Client.new(region: 'us-east-1')

file = File.read('sample-data-2.json')
schedules = JSON.parse(file)
schedules.each{|schedule|

  params = {
      table_name: 'Schedules',
      item: schedule
  }

  begin
    result = dynamodb.put_item(params)
    puts 'Added schedule: ' + {schedule['category']}.to_i.to_s  + ' - ' + {schedule['schedule_name']}

  rescue  Aws::DynamoDB::Errors::ServiceError => error
    puts 'Unable to add schedule:'
    puts error.message
  end
}
