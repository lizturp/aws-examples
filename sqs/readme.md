#Running from Jenkins
# check out repo and cd into dir

aws s3 cp ${QueueName}/queue-policy.template s3://liz-infrastructure-prod/cloudformation/sqs/includes/queue-policy/${QueueName}/queue-policy.template --sse

aws cloudformation deploy --stack-name s${QueueName} --template-file base-sqs.template --capabilities CAPABILITY_NAMED_IAM --parameter-overrides QueueName=${QueueName}
