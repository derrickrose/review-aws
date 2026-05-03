# Movie Recommender - AWS Infrastructure

Cloud infrastructure for movie recommendation system using AWS services: Airflow (MWAA), EMR Serverless, Apache Iceberg, and Jenkins CI/CD.

## Architecture Overview

### Data Processing VPC (10.0.0.0/16)
- **Airflow (MWAA)**: Orchestrates data pipelines
- **EMR Serverless**: Executes Spark jobs (Parquet → Iceberg)
- **Glue Data Catalog**: Manages Iceberg table metadata
- **S3**: Data lake storage

### CI/CD VPC (10.1.0.0/16) - Optional
- **Jenkins**: Build and deployment automation
- **VPC Peering**: Connects to Data VPC when needed

## Project Structure

```
projects/
├── 00-s3-cloudtrail/          # S3 bucket + CloudTrail for audit logging
├── 00-s3-datalake/            # S3 bucket for datalake (Parquet & Iceberg warehouse)
├── 00-s3-logs/                # S3 bucket for application logs
├── 00-s3-mwaa/                # S3 bucket for Airflow DAGs/plugins
├── 01-vpc-data-processing/    # Data processing VPC (10.0.0.0/16)
├── 01-vpc-devops/             # DevOps CI/CD VPC (10.1.0.0/16)
├── 01-vpc-peering/            # VPC peering (DevOps ↔ Data VPC)
├── 03-iam-emr/                # IAM role for EMR Serverless (shared)
├── 03-iam-mwaa/               # IAM role for Airflow
├── 04-mwaa/                   # Airflow environment + config files + pre-deploy script
└── 05-emr-serverless/         # EMR Serverless + Glue database
```

## Deployment Guide

### Phase 1: Data Processing Infrastructure

Deploy in this exact order:

#### 1. S3 Buckets & CloudTrail (Infrastructure Layer)
```bash
# CloudTrail bucket + CloudTrail (audit logging)
aws cloudformation deploy \
  --template-file projects/00-s3-cloudtrail/template.yaml \
  --stack-name dev-miketriky-s3-cloudtrail \
  --parameter-overrides Env=dev

# Datalake bucket (for Parquet/Iceberg)
aws cloudformation deploy \
  --template-file projects/00-s3-datalake/template.yaml \
  --stack-name dev-miketriky-s3-datalake \
  --parameter-overrides Env=dev

# Logs bucket (for application logs)
aws cloudformation deploy \
  --template-file projects/00-s3-logs/template.yaml \
  --stack-name dev-miketriky-s3-logs \
  --parameter-overrides Env=dev

# MWAA bucket (for DAGs/plugins)
aws cloudformation deploy \
  --template-file projects/00-s3-mwaa/template.yaml \
  --stack-name dev-miketriky-s3-mwaa \
  --parameter-overrides Env=dev
```

#### 2. Data Processing VPC
```bash
aws cloudformation deploy \
  --template-file projects/01-vpc-data-processing/template.yaml \
  --stack-name dev-miketriky-vpc \
  --parameter-overrides Env=dev
```

#### 3. IAM Roles
```bash
# MWAA execution role
aws cloudformation deploy \
  --template-file projects/03-iam-mwaa/template.yaml \
  --stack-name dev-miketriky-iam-mwaa \
  --parameter-overrides Env=dev \
  --capabilities CAPABILITY_NAMED_IAM

# EMR Serverless execution role (shared across all EMR apps)
aws cloudformation deploy \
  --template-file projects/03-iam-emr/template.yaml \
  --stack-name dev-miketriky-iam-emr \
  --parameter-overrides Env=dev \
  --capabilities CAPABILITY_NAMED_IAM
```

#### 4. Airflow Environment

**Important**: Run pre-deploy script first to upload MWAA config files to S3:

```bash
cd projects/04-mwaa
./pre-deploy.sh dev eu-west-3
cd ../..
```

Then deploy the MWAA stack:

```bash
aws cloudformation deploy \
  --template-file projects/04-mwaa/template.yaml \
  --stack-name dev-miketriky-mwaa \
  --parameter-overrides Env=dev AirflowVersion=3.0.6
```

#### 5. EMR Serverless
```bash
aws cloudformation deploy \
  --template-file projects/05-emr-serverless/template.yaml \
  --stack-name dev-miketriky-emr-serverless \
  --parameter-overrides Env=dev
```

### Phase 2: DevOps Infrastructure (Optional)

Deploy when you need Jenkins:

#### 6. DevOps VPC
```bash
aws cloudformation deploy \
  --template-file projects/01-vpc-devops/template.yaml \
  --stack-name dev-miketriky-devops-vpc \
  --parameter-overrides Env=dev
```

#### 7. VPC Peering (Connect DevOps to Data VPC)
```bash
aws cloudformation deploy \
  --template-file projects/01-vpc-peering/template.yaml \
  --stack-name dev-miketriky-vpc-peering \
  --parameter-overrides Env=dev
```

## Resource Naming Convention

All resources follow this pattern:

- **IAM Roles**: `{env}-miketriky-common-{service}-role`
  - Example: `dev-miketriky-common-emr-serverless-role`
- **Applications**: `{env}-miketriky-{project}-{service}`
  - Example: `dev-miketriky-parquet-to-iceberg-emr`
- **S3 Buckets**: `{env}-miketriky-{purpose}-{region}`
  - Example: `dev-miketriky-data-eu-west-3`
- **Glue Database**: `{env}_miketriky_{purpose}_db`
  - Example: `dev_miketriky_iceberg_db`

## Network Configuration

### Data VPC (10.0.0.0/16)
| Subnet Type | AZ | CIDR | Purpose |
|-------------|-------|---------------|---------|
| Private A | eu-west-3a | 10.0.0.0/24 | Airflow, EMR |
| Private B | eu-west-3b | 10.0.1.0/24 | Airflow, EMR |
| Public A | eu-west-3a | 10.0.100.0/24 | NAT Gateway |
| Public B | eu-west-3b | 10.0.101.0/24 | NAT Gateway |

### DevOps VPC (10.1.0.0/16)
| Subnet Type | AZ | CIDR | Purpose |
|-------------|-------|---------------|---------|
| Private A | eu-west-3a | 10.1.0.0/24 | Jenkins agents |
| Private B | eu-west-3b | 10.1.1.0/24 | Jenkins agents |
| Public A | eu-west-3a | 10.1.100.0/24 | ALB, NAT Gateway |
| Public B | eu-west-3b | 10.1.101.0/24 | ALB, NAT Gateway |

## Key Resources Created

### Airflow (MWAA)
- **Environment**: `dev-miketriky-mwaa`
- **Version**: 3.0.6
- **Capacity (dev)**: 1-2 workers, 2 schedulers
- **Access**: Public web UI
- **S3 Bucket**: DAGs, plugins, requirements

### EMR Serverless
- **Application**: `dev-miketriky-parquet-to-iceberg-emr`
- **Release**: EMR 7.1.0
- **Capacity (dev)**:
  - Driver: 1 worker (2 vCPU, 4 GB)
  - Executor: 1 worker (4 vCPU, 8 GB)
- **Auto-stop**: 15 minutes idle
- **Iceberg**: Pre-configured with Glue Catalog

### Glue Database
- **Name**: `dev_miketriky_iceberg_db`
- **Purpose**: Stores Iceberg table metadata

### IAM Roles
- **MWAA Role**: `dev-miketriky-mwaa-execution-role`
  - S3 access (MWAA bucket)
  - CloudWatch Logs
  - VPC network interface management

- **EMR Role**: `dev-miketriky-common-emr-serverless-role` (shared)
  - S3 access (read MWAA bucket, read/write data bucket)
  - Glue Catalog access
  - CloudWatch Logs

## Running Spark Jobs

### Example: Submit Job from Airflow

```python
from airflow.providers.amazon.aws.operators.emr import EmrServerlessStartJobOperator

start_job = EmrServerlessStartJobOperator(
    task_id='parquet_to_iceberg',
    application_id='{{ var.value.emr_app_id }}',
    execution_role_arn='{{ var.value.emr_role_arn }}',
    job_driver={
        'sparkSubmit': {
            'entryPoint': 's3://dev-miketriky-mwaa-eu-west-3/spark-jobs/parquet_to_iceberg.py',
            'sparkSubmitParameters': '--conf spark.executor.cores=4'
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

### Example: Spark Job (Parquet → Iceberg)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Parquet to Iceberg") \
    .getOrCreate()

# Read Parquet
df = spark.read.parquet("s3://dev-miketriky-data-eu-west-3/input/*.parquet")

# Write to Iceberg table
df.writeTo("glue_catalog.dev_miketriky_iceberg_db.movies") \
    .using("iceberg") \
    .createOrReplace()

spark.stop()
```

## Stack Outputs

Get stack outputs for reference in other tools:

```bash
# Get EMR Application ID
aws cloudformation describe-stacks \
  --stack-name dev-miketriky-emr-serverless \
  --query 'Stacks[0].Outputs[?OutputKey==`EMRApplicationId`].OutputValue' \
  --output text

# Get EMR Role ARN
aws cloudformation describe-stacks \
  --stack-name dev-miketriky-iam-emr \
  --query 'Stacks[0].Outputs[?OutputKey==`EMRServerlessExecutionRoleArn`].OutputValue' \
  --output text

# Get MWAA Web URL
aws cloudformation describe-stacks \
  --stack-name dev-miketriky-mwaa \
  --query 'Stacks[0].Outputs[?OutputKey==`MWAAWebServerUrl`].OutputValue' \
  --output text
```

## Environment Variables

Supported environments: `dev`, `staging`, `prod`

Each environment has different capacity settings:

| Environment | MWAA Workers | EMR Driver | EMR Executor |
|-------------|--------------|------------|--------------|
| dev | 1-2 | 2 vCPU, 4 GB | 4 vCPU, 8 GB |
| staging | 1-5 | 2 vCPU, 4 GB | 4 vCPU, 8 GB (x2) |
| prod | 2-10 | 4 vCPU, 8 GB | 8 vCPU, 16 GB (x4) |

## Cost Optimization

- ✅ EMR Serverless auto-stop after 15 min idle (no cost when idle)
- ✅ MWAA minimum workers configuration
- ✅ S3 Intelligent-Tiering after 30 days (datalake)
- ✅ S3 lifecycle policies:
  - Datalake: Old versions deleted after 30 days
  - Logs: Glacier after 90 days, deleted after 365 days
  - CloudTrail: Glacier after 13 days, deleted after 30 days
- ✅ S3 VPC endpoints (no NAT charges for S3 traffic)
- ✅ CloudTrail multi-region (1st trail free for management events)

## Troubleshooting

### MWAA Environment fails to create
- Check VPC has at least 2 private subnets in different AZs
- Verify security group allows self-referencing traffic
- Ensure S3 bucket exists and is in same region

### EMR Serverless job fails with permission error
- Verify IAM role has S3 and Glue permissions
- Check bucket names match expected pattern
- Ensure Glue database exists

### Can't access MWAA web UI
- Check WebserverAccessMode is PUBLIC_ONLY
- Verify IAM user has MWAA permissions
- Environment must be in AVAILABLE state

### Network connectivity issues
- Verify NAT Gateways are deployed
- Check route tables have correct routes
- Ensure S3 VPC endpoint is attached to private route tables

## Security Best Practices

✅ All data workloads in private subnets
✅ Separate VPCs for CI/CD and data processing
✅ IAM roles follow least privilege principle
✅ S3 buckets have encryption enabled
✅ S3 buckets block all public access
✅ Security groups allow only required traffic

## Cleanup

Delete stacks in reverse order:

```bash
# Phase 2 (if deployed)
aws cloudformation delete-stack --stack-name dev-miketriky-vpc-peering
aws cloudformation delete-stack --stack-name dev-miketriky-devops-vpc

# Phase 1
aws cloudformation delete-stack --stack-name dev-miketriky-emr-serverless
aws cloudformation delete-stack --stack-name dev-miketriky-mwaa
aws cloudformation delete-stack --stack-name dev-miketriky-iam-emr
aws cloudformation delete-stack --stack-name dev-miketriky-iam-mwaa
aws cloudformation delete-stack --stack-name dev-miketriky-vpc

# S3 Buckets (delete last after emptying)
aws s3 rm s3://dev-miketriky-eu-west-3-mwaa --recursive
aws cloudformation delete-stack --stack-name dev-miketriky-s3-mwaa

aws s3 rm s3://dev-miketriky-logs-eu-west-3 --recursive
aws cloudformation delete-stack --stack-name dev-miketriky-s3-logs

aws s3 rm s3://dev-miketriky-datalake-eu-west-3 --recursive
aws cloudformation delete-stack --stack-name dev-miketriky-s3-datalake

aws s3 rm s3://dev-miketriky-cloudtrail-eu-west-3 --recursive
aws cloudformation delete-stack --stack-name dev-miketriky-s3-cloudtrail
```

**Note**: S3 buckets must be emptied before deletion, or the CloudFormation stack deletion will fail.

## Support

For issues with specific components, see:
- EMR Serverless: `projects/05-emr-serverless/README.md`
- AWS Documentation: https://docs.aws.amazon.com/

## License

This project contains CloudFormation templates for AWS infrastructure deployment.

---

## Additional Tools

### SAM CLI Installation
Requirements install SAM:
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

### Packaging
Uses SAM (Serverless Application Manager) to package the lambda function
