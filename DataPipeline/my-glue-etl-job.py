import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1760872947757 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://my-ft-data/raw/"], "recurse": True}, transformation_ctx="AmazonS3_node1760872947757")

# Script generated for node Change Schema
ChangeSchema_node1760872977666 = ApplyMapping.apply(frame=AmazonS3_node1760872947757, mappings=[("step", "string", "step", "int"), ("type", "string", "type", "string"), ("amount", "string", "amount", "string"), ("nameorig", "string", "nameorig", "string"), ("oldbalanceorg", "string", "oldbalanceorg", "float"), ("newbalanceorig", "string", "newbalanceorig", "float"), ("namedest", "string", "namedest", "string"), ("oldbalancedest", "string", "oldbalancedest", "float"), ("newbalancedest", "string", "newbalancedest", "float"), ("isfraud", "string", "isfraud", "int"), ("isflaggedfraud", "string", "isflaggedfraud", "int")], transformation_ctx="ChangeSchema_node1760872977666")

# Script generated for node Drop Duplicates
DropDuplicates_node1760872983056 =  DynamicFrame.fromDF(ChangeSchema_node1760872977666.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1760872983056")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropDuplicates_node1760872983056, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1760872862987", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1760872988518 = glueContext.write_dynamic_frame.from_options(frame=DropDuplicates_node1760872983056, connection_type="s3", format="glueparquet", connection_options={"path": "s3://my-ft-data/processed/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1760872988518")

job.commit()