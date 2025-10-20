# EventDriven-ETL-Pipeline

Overview

An automated serverless AWS data pipeline that:
Detects file uploads to Amazon S3
Triggers AWS Lambda via EventBridge (or S3 Event Notification)
Starts an AWS Glue ETL Job to transform raw data
Optionally launches a Glue Crawler to refresh schema
Writes processed data to S3
Updates the Glue Data Catalog
Makes data immediately queryable in Amazon Athena
This pipeline is fully event-driven — no manual runs required. Perfect for building near real-time ingestion pipelines for structured data.


Architecture
text
S3 (raw data upload)
⬇
EventBridge / S3 Event Notification
⬇
AWS Lambda (Orchestrator)
⬇
AWS Glue ETL Job
⬇
S3 (processed data)
⬇
Glue Crawler → Glue Data Catalog
⬇
Amazon Athena
Repository Structure
text



EventDriven-ETL-Pipeline/
│
├── lambda/
│   └── triggerGlueWorkflow.py                  # Lambda function code to start Glue workflow
│
├── glue/
│   └── glue_etl_job.py                         # AWS Glue job script for ETL
│
├── iam_policies/
│   ├── lambda_execution_policy.json            # Lambda execution policy
│   ├── glue_execution_policy.json              # Glue execution policy
│   ├── trust_relationship_lambda.json          # Lambda trust policy
│   ├── trust_relationship_glue.json            # Glue trust policy
│
├── eventbridge/
│   └── eventbridge_rule.json                   # EventBridge rule for triggering Lambda
│
├── docs/
│   ├── README.md                               # Documentation
│   └── screenshots/
│       ├── s3_upload_event.png
│       ├── lambda_trigger.png
│       ├── glue_job_run.png
│       ├── crawler_catalog_update.png
│       └── athena_query_result.png
│
└── athena_queries/
├── create_table.sql                        # Athena table DDL
├── sample_queries.sql                      # Query examples


Step-by-Step Setup

1.	S3 Bucket & Event Notification
Create an S3 bucket, e.g., my-ft-data
Add folders:
/raw/ for uploads
/processed/ for ETL outputs
Configure Event Notification:
Event Type: All object create events
Prefix: raw/
Suffix: .csv
Destination: Lambda function triggerGlueWorkflow

3.	Lambda Function
Code: triggerGlueWorkflow.py
Environment Variable:
text
GLUE_WORKFLOW_NAME = my-etl-project
IAM Role Permissions:
Attach lambda_execution_policy.json and trust_relationship_lambda.json
Allow S3 to Invoke Lambda:
text
aws lambda add-permission   
--function-name triggerGlueWorkflow   
--statement-id s3invoke   
--action lambda:InvokeFunction   
--principal s3.amazonaws.com   
--source-arn arn:aws:s3:::my-ft-data

5. AWS Glue Workflow & ETL Job
ETL Script: glue_etl_job.py
IAM Role: Attach glue_execution_policy.json and trust_relationship_glue.json
This job:
Reads raw CSV data from s3://my-ft-data/raw/
Applies schema mapping
Removes duplicates and null fields
Evaluates data quality rules
Writes transformed data in Parquet (Snappy) to s3://my-ft-data/processed/
Workflow triggers a Glue Crawler:
Scans processed folder
Updates Glue Data Catalog for Athena queries

6.	AWS Glue Crawler
Target: s3://my-ft-data/processed/
Database: my_investigation_db
Schedule: On-demand or triggered by workflow
Output: Table visible in Glue Data Catalog

7.	Athena Integration
Run the following SQLs from athena_queries/:
Create Table: create_table.sql
Sample Queries: sample_queries.sql
Query processed data directly via Athena console.
Testing the Pipeline
Upload Fraud.csv to s3://my-ft-data/raw/
Event triggers Lambda → starts Glue workflow
Glue job processes the file and writes output to processed/
Crawler updates schema in Data Catalog
Query data using Athena
Troubleshooting
Refer to docs/troubleshooting.md covering:
Lambda invocation issues
Glue job success but empty output
Crawler "no tables created" issue
Missing Athena schema
Technologies Used
Amazon S3
AWS EventBridge
AWS Lambda
AWS Glue (Workflow, Job, Crawler)
AWS IAM
Amazon Athena
AWS CloudWatch
Credits & Acknowledgements
Project developed by Vibin Krishna
Guided and refined using AWS Documentation and Perplexity AI support (2025)
