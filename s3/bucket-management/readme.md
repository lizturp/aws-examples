** Bucket Policy vs. IAM Policy **

2 good articles that cover the basics:

https://aws.amazon.com/blogs/security/iam-policies-and-bucket-policies-and-acls-oh-my-controlling-access-to-s3-resources/
https://docs.aws.amazon.com/AmazonS3/latest/dev/intro-managing-access-s3-resources.html


** Cloudformation Template - S3 Bucket **

How to use the S3 bucket CF template

```s3 > bucket-management```

1. create a new folder using the name of your bucket
2. create a project.properties file
	a. use liz-coolproject-dev as an example
3. create a lifecycle.template file
	a. add in the lifecycle policy as defined by business owner for project

additional step for buckets that *require cross account access* - Skip to Step 5 if not interacting with another AWS account

4. Create custom template
	a.  see example: "example-template-for-cross-account-access-only.template"
5. merge final updates into development branch
6. Go to Jenkins AWS > Dev Tools Dashboard
	a. Build with Parameters (bucketname and Env.)


# FROM JENKINS 
cd s3/bucket-management/${BUCKETNAME}
aws s3 cp lifecycle.template s3://liz-infrastructure-prod/cloudformation/s3/includes/lifecycle/${BUCKETNAME}/lifecycle.template --sse
source project.properties
cd ../
aws cloudformation validate-template --template-body file://s3-bucket.template
aws cloudformation deploy --stack-name s3-${ENV}-${BUCKETNAME} --template-file s3-bucket.template --capabilities CAPABILITY_NAMED_IAM --parameter-overrides ProjectName=${PROJECTNAME} Environment=${ENV} BucketName=${BUCKETNAME}
