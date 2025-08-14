import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.gluetypes import *
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def _find_null_fields(ctx, schema, path, output, nullStringSet, nullIntegerSet, frame):
    if isinstance(schema, StructType):
        for field in schema:
            new_path = path + "." if path != "" else path
            output = _find_null_fields(ctx, field.dataType, new_path + field.name, output, nullStringSet, nullIntegerSet, frame)
    elif isinstance(schema, ArrayType):
        if isinstance(schema.elementType, StructType):
            output = _find_null_fields(ctx, schema.elementType, path, output, nullStringSet, nullIntegerSet, frame)
    elif isinstance(schema, NullType):
        output.append(path)
    else:
        x, distinct_set = frame.toDF(), set()
        for i in x.select(path).distinct().collect():
            distinct_ = i[path.split('.')[-1]]
            if isinstance(distinct_, list):
                distinct_set |= set([item.strip() if isinstance(item, str) else item for item in distinct_])
            elif isinstance(distinct_, str) :
                distinct_set.add(distinct_.strip())
            else:
                distinct_set.add(distinct_)
        if isinstance(schema, StringType):
            if distinct_set.issubset(nullStringSet):
                output.append(path)
        elif isinstance(schema, IntegerType) or isinstance(schema, LongType) or isinstance(schema, DoubleType):
            if distinct_set.issubset(nullIntegerSet):
                output.append(path)
    return output

def drop_nulls(glueContext, frame, nullStringSet, nullIntegerSet, transformation_ctx) -> DynamicFrame:
    nullColumns = _find_null_fields(frame.glue_ctx, frame.schema(), "", [], nullStringSet, nullIntegerSet, frame)
    return DropFields.apply(frame=frame, paths=nullColumns, transformation_ctx=transformation_ctx)

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
AmazonS3_node1754810143057 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://fba-investigation/raw/"], "recurse": True}, transformation_ctx="AmazonS3_node1754810143057")

# Script generated for node Drop Duplicates
DropDuplicates_node1754810171051 =  DynamicFrame.fromDF(AmazonS3_node1754810143057.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1754810171051")

# Script generated for node Drop Null Fields
DropNullFields_node1754810187654 = drop_nulls(glueContext, frame=DropDuplicates_node1754810171051, nullStringSet={}, nullIntegerSet={}, transformation_ctx="DropNullFields_node1754810187654")

# Script generated for node Change Schema
ChangeSchema_node1754810253158 = ApplyMapping.apply(frame=DropNullFields_node1754810187654, mappings=[("transaction_id", "string", "transaction_id", "string"), ("seller_id", "string", "seller_id", "string"), ("customer_id", "string", "customer_id", "string"), ("product_sku", "string", "product_sku", "string"), ("transaction_date", "string", "transaction_date", "string"), ("transaction_amount", "string", "transaction_amount", "string"), ("shipping_address", "string", "shipping_address", "string"), ("return_status", "string", "return_status", "string")], transformation_ctx="ChangeSchema_node1754810253158")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1754810253158, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1754810100637", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1754810265437 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1754810253158, connection_type="s3", format="glueparquet", connection_options={"path": "s3://fba-investigation/processed/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1754810265437")

job.commit()