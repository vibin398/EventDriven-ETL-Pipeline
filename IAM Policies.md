 S3AccessPolicy 

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "S3ReadWriteAccess",
			"Effect": "Allow",
			"Action": [
				"s3:ListBucket",
				"s3:GetObject",
				"s3:PutObject",
				"s3:DeleteObject"
			],
			"Resource": [
				"arn:aws:s3:::my-ft-data",
				"arn:aws:s3:::my-ft-data/*"
			]
		},
		{
			"Sid": "AllowGlueTransformsBucketAccess",
			"Effect": "Allow",
			"Action": [
				"s3:GetObject",
				"s3:ListBucket"
			],
			"Resource": [
				"arn:aws:s3:::aws-glue-studio-transforms-584702181950-prod-ap-south-1",
				"arn:aws:s3:::aws-glue-studio-transforms-584702181950-prod-ap-south-1/*"
			]
		},
		{
			"Sid": "AllowGlueAssetsBucketAccess",
			"Effect": "Allow",
			"Action": [
				"s3:GetObject",
				"s3:ListBucket"
			],
			"Resource": [
				"arn:aws:s3:::aws-glue-assets-111238651186-ap-south-1",
				"arn:aws:s3:::aws-glue-assets-111238651186-ap-south-1/*"
			]
		}
	]
}


LambdaExecutionandCloudWatchLoggingPolicy

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "CloudWatchLogs",
			"Effect": "Allow",
			"Action": [
				"logs:CreateLogGroup",
				"logs:CreateLogStream",
				"logs:PutLogEvents"
			],
			"Resource": "*"
		},
		{
			"Sid": "CloudWatchMetrics",
			"Effect": "Allow",
			"Action": [
				"cloudwatch:PutMetricData"
			],
			"Resource": "*"
		}
	]
}

GLUE DB
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"glue:GetDatabase",
				"glue:GetDatabases",
				"glue:GetTable",
				"glue:GetTables",
				"glue:GetPartition",
				"glue:GetPartitions",
				"glue:CreateTable",
				"glue:UpdateTable"
			],
			"Resource": [
				"arn:aws:glue:ap-south-1:111238651186:catalog",
				"arn:aws:glue:ap-south-1:111238651186:database/my_investigation_db",
				"arn:aws:glue:ap-south-1:111238651186:table/my_investigation_db/*"
			]
		}
	]
}

AWSGlueJobManagementPolicy 

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "GlueJobExecution",
			"Effect": "Allow",
			"Action": [
				"glue:StartJobRun",
				"glue:StartWorkflowRun",
				"glue:GetJobRun",
				"glue:GetWorkflowRun"
			],
			"Resource": "*"
		}
	]
}

 AthenaQueryExecutionPolicy

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "EventBridgeManagement",
			"Effect": "Allow",
			"Action": [
				"events:PutRule",
				"events:PutTargets",
				"events:EnableRule",
				"events:DisableRule",
				"events:DescribeRule"
			],
			"Resource": "*"
		},
		{
			"Sid": "InvokeLambda",
			"Effect": "Allow",
			"Action": "lambda:InvokeFunction",
			"Resource": "arn:aws:lambda:ap-south-1:111238651186:function:learningpython"
		}
	]
}