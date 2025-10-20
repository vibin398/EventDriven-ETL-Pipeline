import json
import boto3
import os
from botocore.exceptions import ClientError

glue = boto3.client('glue', region_name='ap-south-1')
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

def lambda_handler(event, context):
    workflow_name = "etl_pipeline_workflow"

    try:
        response = glue.start_workflow_run(Name=workflow_name)
        run_id = response['RunId']
        print(f"Started Glue Workflow: {workflow_name} - RunId: {run_id}")

        # Send custom CloudWatch metric for monitoring workflow start
        cloudwatch.put_metric_data(
            Namespace='ETLPipeline',
            MetricData=[
                {
                    'MetricName': 'WorkflowTriggered',
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Workflow {workflow_name} triggered! RunId: {run_id}")
        }

    except ClientError as e:
        print("Glue client error:", e)
        # Send metric for failed workflow start
        cloudwatch.put_metric_data(
            Namespace='ETLPipeline',
            MetricData=[
                {
                    'MetricName': 'WorkflowTriggerFailures',
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
        raise

    except Exception as e:
        print("Other error:", e)
        raise

