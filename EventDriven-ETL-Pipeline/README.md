

# **EventDriven-ETL-Pipeline**

## **Overview**
An automated **serverless AWS data pipeline** that:
1. Detects file uploads to Amazon S3  
2. Triggers AWS Lambda via S3 Event Notification (or EventBridge)  
3. Starts an AWS Glue ETL Job (and optionally a Glue Crawler)  
4. Stores processed data back in S3  
5. Updates the AWS Glue Data Catalog  
6. Makes the data **immediately queryable in Athena**.

This pipeline is fully **event-driven** — no manual job runs needed.

***

## **Architecture**

S3 (raw file upload)  
&nbsp;&nbsp;⬇  
**Event Notification / EventBridge**  
&nbsp;&nbsp;⬇  
**AWS Lambda** – [`triggerGlueJobFunction.py`](../lambda/triggerGlueJobFunction.py)  
&nbsp;&nbsp;⬇  
**AWS Glue Job** – [`glue_job_script.py`](../glue/glue_job_script.py)  
&nbsp;&nbsp;⬇  
S3 (processed data)  
&nbsp;&nbsp;⬇  
**Glue Crawler → Glue Data Catalog**  
&nbsp;&nbsp;⬇  
**Amazon Athena** Queries – [`athena_queries/sample_queries.sql`](../athena_queries/sample_queries.sql)

![Architecture Diagram](docs/architectureFolder Structure**

```
EventDriven-ETL-Pipeline/
│
├── lambda/
│   └── triggerGlueJobFunction.py           # Lambda function code
│
├── glue/
│   └── glue_job_script.py                  # Glue ETL job script
│
├── iam_policies/
│   ├── lambda_execution_role_policy.json   # IAM policy for Lambda execution
│   ├── glue_execution_role_policy.json     # IAM policy for Glue
│   ├── trust_relationship_lambda.json      # Trust relationship for Lambda role
│   ├── trust_relationship_glue.json        # Trust relationship for Glue role
│
├── eventbridge/
│   └── eventbridge_rule_pattern.json       # EventBridge pattern for S3 trigger
│
├── docs/
│   ├── README.md                           # This documentation
│   └── screenshots/                        # All screenshots
│       ├── s3_event_notification.png
│       ├── lambda_config.png
│       ├── glue_workflow_run.png
│       ├── athena_query_result.png
│       └── ...
│
└── athena_queries/
    ├── create_table.sql                    # Athena table creation DDL
    ├── sample_queries.sql                   # Athena example queries
```

***

## **Step-by-Step Setup**

### **1. S3 Bucket & Event Notification**
- Create S3 bucket `fba-investigation`
- Organize raw uploads in `raw/` prefix
- Add Event Notification:
  - Event type: **All object create events**
  - Prefix: `raw/`
  - Suffix: `.csv`
  - Destination: Lambda function `triggerGlueJobFunction`  
  *(Screenshot: [s3_event_notification.png](docs/screenshots/s3_event_notification.png))*

***

### **2. Lambda Function**
- Code: [`triggerGlueJobFunction.py`](lambda/triggerGlueJobFunction.py)
- Environment variable: `GLUE_JOB_NAME = my-refining-job`
- Role Permissions: [`lambda_execution_role_policy.json`](iam_policies/lambda_execution_role_policy.json) + [`trust_relationship_lambda.json`](iam_policies/trust_relationship_lambda.json)
- Allow S3 to invoke Lambda:
```bash
aws lambda add-permission \
  --function-name triggerGlueJobFunction \
  --statement-id s3invoke \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::fba-investigation
```
*(Screenshot: [lambda_config.png](docs/screenshots/lambda_config.png))*

***

### **3. AWS Glue ETL Job & Crawler**
- ETL Script: [`glue_job_script.py`](glue/glue_job_script.py)
- IAM Role for Glue: [`glue_execution_role_policy.json`](iam_policies/glue_execution_role_policy.json) + [`trust_relationship_glue.json`](iam_policies/trust_relationship_glue.json)
- Output to processed S3 location
- Glue Crawler updates Glue Data Catalog for Athena

***

### **4. Athena Table**
- Create table SQL: [`create_table.sql`](athena_queries/create_table.sql)
- Test queries: [`sample_queries.sql`](athena_queries/sample_queries.sql)  
*(Screenshot: [athena_query_result.png](docs/screenshots/athena_query_result.png))*

***

## **Testing the Pipeline**
1. Upload a `.csv` file to `s3://fba-investigation/raw/`
2. Check CloudWatch Logs for Lambda execution
3. Verify Glue Job run in AWS Glue Console
4. Confirm processed file in `processed/` S3 path
5. Query in Athena

***

## **Troubleshooting**
See full guide: [`troubleshooting.md`](docs/troubleshooting.md)  
Covers:
- Lambda not triggering
- Glue job permissions errors
- Crawler internal service exceptions
- Athena schema issues

***

## **Technologies**
- Amazon S3
- AWS EventBridge
- AWS Lambda
- AWS Glue (ETL + Crawler)
- AWS IAM
- Amazon Athena

***

## Credits and Acknowledgements

- Project Created and Documented by Vibin Krishna 
- Guided and Supported by AWS Official Documentation and AI (Perplexity AI)
