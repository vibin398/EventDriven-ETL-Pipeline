# Event-Driven ETL Pipeline on AWS

## Overview

This project demonstrates a fully automated, serverless ETL pipeline on AWS using S3, Lambda, Glue (ETL jobs and crawlers), Glue Data Catalog, Amazon Athena, and CloudWatch Alarms.

**Workflow:**
- Data is uploaded to an S3 bucket (`my-ft-data/raw/`).
- S3 Event Notification (or EventBridge) triggers a Lambda function.
- Lambda initiates an AWS Glue ETL Job, which processes raw data and writes processed Parquet files to `my-ft-data/processed/`.
- An AWS Glue Crawler scans the processed data and updates the Glue Data Catalog.
- The data is now queryable instantly using Amazon Athena.
- CloudWatch alarms notify when workflow steps fail.

## Architecture

S3 (raw file upload)
⬇
Event Notification / EventBridge
⬇
AWS Lambda
⬇
AWS Glue ETL Job
⬇
S3 (processed data)
⬇
Glue Crawler → Glue Data Catalog
⬇
Amazon Athena
⬇
CloudWatch Alarms (monitoring across all steps)


_Screenshot highlights stored in `/docs/screenshots/`_

## Repository Structure

EventDriven-ETL-Pipeline/
│
├── lambda/
│ └── triggerGlueWorkflow.py
│
├── glue/
│ └── glue_etl_job.py
│
├── iam_policies/
│ ├── lambda_execution_policy.json
│ ├── glue_execution_policy.json
│ ├── trust_relationship_lambda.json
│ ├── trust_relationship_glue.json
│
├── eventbridge/
│ └── eventbridge_rule.json
│
├── docs/
│ ├── README.md
│ └── screenshots/
│ ├── [S3, Lambda, Glue, Athena, Crawler, Alarm screenshots]
│
└── athena_queries/
├── create_table.sql
├── sample_queries.sql


## CloudWatch Alarms: End-to-End Monitoring

- **Glue Job Failure Alarm:** Triggers when any Glue ETL job fails.
- **Glue Crawler Failure Alarm:** Triggers if crawler run fails.
- **Lambda Error Alarm:** Triggers if Lambda function throws errors or is throttled.
- **Workflow Failure/Trigger Alarms:** Monitor overall Glue workflow failures and invocations.
- **SNS Email Notification:** Alarms send emails/SMS (see attached screenshot and example notification).

> For each resource, create a CloudWatch alarm based on `FailedRuns` (Glue), `FailedCrawls` (Crawler), `Errors/Throttles` (Lambda), and specific custom metrics for workflow state.

## Step-by-Step Setup

1. **Create S3 Bucket**  
   - `my-ft-data` with `raw/` for uploads, `processed/` for Glue output.

2. **Configure S3 Event Notification or EventBridge**  
   - Event type: Object created
   - Prefix: `raw/`
   - Suffix: `.csv`
   - Destination: Lambda function

3. **Lambda Function**
   - Environment variable: `GLUE_WORKFLOW_NAME`
   - IAM: Attach `lambda_execution_policy.json`
   - Allow S3 to trigger Lambda

4. **Glue ETL Job**
   - Input: `s3://my-ft-data/raw/`
   - Output: `s3://my-ft-data/processed/` (Parquet+Snappy)
   - IAM: Attach `glue_execution_policy.json`

5. **Glue Crawler**
   - Scans: `s3://my-ft-data/processed/`
   - Updates database: `my_investigation_db`

6. **Athena Integration**
   - Point to Glue Data Catalog database
   - Use SQL scripts in `athena_queries/`

7. **Configure CloudWatch Alarms**
   - For each job, crawler, Lambda, and workflow step
   - Link to SNS topic for notification

## Usage

1. Upload a CSV file to your S3 bucket’s `raw/` folder.
2. Your Lambda function triggers and starts the Glue ETL pipeline.
3. Processed results are written to the `processed/` folder.
4. The Glue crawler updates the Glue Data Catalog with schema from processed files.
5. Query your data instantly via Athena.
6. Receive email/SMS if the process fails at any stage.

## Screenshots

- S3 processed data files
- Glue workflow visualization and status
- Glue ETL job and Crawler run histories
- Athena table and query output
- CloudWatch alarm dashboard and SNS notification email

*(See images in `/docs/screenshots/`)*

This project demonstrates an optimized, event-driven ETL pipeline running on AWS Glue that processes and crawls 600,000 rows in just 2.42 seconds. It showcases advanced data orchestration and automation using AWS services including Glue workflows, Lambda, and CloudWatch, delivering scalable, fast, and cost-efficient data processing with clear metrics proving substantial performance gains.

## Technologies

- Amazon S3, EventBridge, Lambda, Glue (ETL, Crawler, Data Catalog, Workflow)
- Amazon Athena, CloudWatch Alarms, SNS, IAM

## Credits

Project created and maintained by **Vibin Krishna**  
With guidance from AWS Documentation and Perplexity AI


