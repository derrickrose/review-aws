# EMR Serverless - Parquet to Iceberg

## Overview
This stack creates EMR Serverless infrastructure for reading Parquet files from S3 and writing to Apache Iceberg tables.

## Stack Deployment Order

### Prerequisites (Must be deployed first):
1. `00-data-processing-vpc` - VPC with private subnets and security groups
2. `01-s3-mwaa` - MWAA S3 bucket (for reading Parquet files)

### EMR Infrastructure (Deploy in this order):
1. `01-datalake-s3` - S3 bucket for EMR data and Iceberg warehouse
2. `03-iam-emr` - IAM execution role for EMR Serverless
3. `05-emr-serverless` - EMR Serverless application with Iceberg support

## Deployment Commands

```bash
# Deploy S3 data lake bucket
aws cloudformation deploy \
  --template-file projects/01-s3-datalake/template.yaml \
  --stack-name dev-miketriky-datalake-s3 \
  --parameter-overrides Env=dev

# Deploy IAM role
aws cloudformation deploy \
  --template-file projects/03-iam-emr/template.yaml \
  --stack-name dev-miketriky-iam-emr \
  --parameter-overrides Env=dev \
  --capabilities CAPABILITY_NAMED_IAM

# Deploy EMR Serverless application
aws cloudformation deploy \
  --template-file projects/05-emr-serverless/template.yaml \
  --stack-name dev-miketriky-emr-serverless \
  --parameter-overrides Env=dev
```

## Resources Created

### 1. Glue Database
- **Name**: `dev_miketriky_iceberg_db`
- **Purpose**: Stores Iceberg table metadata

### 2. EMR Serverless Application
- **Name**: `dev-miketriky-parquet-to-iceberg-emr`
- **Release**: EMR 7.1.0
- **Type**: Spark
- **Capacity (dev)**:
  - Driver: 1 worker (2 vCPU, 4 GB)
  - Executor: 1 worker (4 vCPU, 8 GB)
- **Auto-stop**: 15 minutes idle timeout
- **Network**: Private subnets (eu-west-3a, eu-west-3b)

### 3. IAM Role
- **Name**: `dev-miketriky-common-emr-serverless-role`
- **Permissions**:
  - Read from MWAA S3 bucket
  - Read/write to data S3 bucket
  - Full Glue Catalog access
  - CloudWatch Logs

### 4. S3 Bucket
- **Name**: `dev-miketriky-data-eu-west-3`
- **Iceberg Warehouse**: `s3://dev-miketriky-data-eu-west-3/iceberg-warehouse/`

## Running Spark Jobs

When submitting jobs from Airflow or AWS CLI, you need to:

1. **Specify the execution role ARN** (exported as `dev-miketriky-common-emr-serverless-role-arn`)
2. **Reference the application ID** (exported as `dev-miketriky-parquet-to-iceberg-emr-app-id`)

### Example: Submit Job via AWS CLI

```bash
aws emr-serverless start-job-run \
  --application-id <app-id-from-cloudformation-output> \
  --execution-role-arn arn:aws:iam::<account-id>:role/dev-miketriky-common-emr-serverless-role \
  --job-driver '{
    "sparkSubmit": {
      "entryPoint": "s3://dev-miketriky-mwaa-eu-west-3/spark-jobs/parquet-to-iceberg.py",
      "sparkSubmitParameters": "--conf spark.executor.cores=4 --conf spark.executor.memory=8g"
    }
  }'
```

### Example: Airflow DAG with EMRServerlessStartJobOperator

```python
from airflow.providers.amazon.aws.operators.emr import EmrServerlessStartJobOperator

start_job = EmrServerlessStartJobOperator(
    task_id='parquet_to_iceberg_job',
    application_id='{{ var.value.emr_app_id }}',  # From CloudFormation output
    execution_role_arn='{{ var.value.emr_execution_role_arn }}',  # From CloudFormation output
    job_driver={
        'sparkSubmit': {
            'entryPoint': 's3://dev-miketriky-mwaa-eu-west-3/spark-jobs/parquet-to-iceberg.py',
            'sparkSubmitParameters': '--conf spark.executor.cores=4 --conf spark.executor.memory=8g'
        }
    },
    configuration_overrides={
        'monitoringConfiguration': {
            's3MonitoringConfiguration': {
                'logUri': 's3://dev-miketriky-data-eu-west-3/emr-logs/'
            }
        }
    }
)
```

## Spark Job Example

```python
from pyspark.sql import SparkSession

# Initialize Spark with Iceberg
spark = SparkSession.builder \
    .appName("Parquet to Iceberg") \
    .getOrCreate()

# Read Parquet from S3
parquet_df = spark.read.parquet("s3://dev-miketriky-mwaa-eu-west-3/data/input.parquet")

# Write to Iceberg table
parquet_df.writeTo("glue_catalog.dev_miketriky_iceberg_db.my_table") \
    .using("iceberg") \
    .createOrReplace()

spark.stop()
```

## Stack Outputs

After deployment, get the outputs:

```bash
aws cloudformation describe-stacks \
  --stack-name dev-miketriky-emr-serverless \
  --query 'Stacks[0].Outputs'
```

Key outputs:
- `EMRApplicationId` - Use when submitting jobs
- `EMRApplicationArn` - Application ARN
- `GlueDatabaseName` - Glue database name for Iceberg tables

## Cost Optimization

- Auto-start/stop enabled (no cost when idle)
- Minimum capacity configuration for dev
- Intelligent-Tiering for S3 storage
- 30-day lifecycle for old versions

## Troubleshooting

1. **Job fails with permission errors**: Verify IAM role has correct S3 and Glue permissions
2. **Can't find Glue database**: Check database name is `dev_miketriky_iceberg_db`
3. **Network timeout**: Ensure VPC has S3 endpoint and NAT gateways configured
