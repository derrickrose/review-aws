#!/bin/bash

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENV=${1:-dev}
REGION=${2:-eu-west-3}
BUCKET_NAME="${ENV}-miketriky-${REGION}-mwaa"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}MWAA Pre-Deployment Script${NC}"
echo -e "${YELLOW}========================================${NC}"
echo -e "Environment: ${GREEN}${ENV}${NC}"
echo -e "Region: ${GREEN}${REGION}${NC}"
echo -e "Bucket: ${GREEN}${BUCKET_NAME}${NC}"
echo ""

# Check if bucket exists
echo -e "${YELLOW}[1/5]${NC} Checking if S3 bucket exists..."
if aws s3 ls "s3://${BUCKET_NAME}" 2>&1 | grep -q 'NoSuchBucket'; then
    echo -e "${RED}ERROR: Bucket ${BUCKET_NAME} does not exist!${NC}"
    echo -e "${YELLOW}Please deploy the 00-s3-mwaa stack first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Bucket exists${NC}"
echo ""

# Create dags folder
echo -e "${YELLOW}[2/5]${NC} Creating dags/ folder structure..."
aws s3api put-object --bucket "${BUCKET_NAME}" --key dags/ 2>/dev/null || true
echo -e "${GREEN}✓ dags/ folder created${NC}"
echo ""

# Upload requirements.txt
echo -e "${YELLOW}[3/5]${NC} Uploading requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}ERROR: requirements.txt not found!${NC}"
    exit 1
fi
aws s3 cp requirements.txt "s3://${BUCKET_NAME}/requirements.txt"
echo -e "${GREEN}✓ requirements.txt uploaded${NC}"
echo ""

# Upload startup.sh
echo -e "${YELLOW}[4/5]${NC} Uploading startup.sh..."
if [ ! -f "startup.sh" ]; then
    echo -e "${RED}ERROR: startup.sh not found!${NC}"
    exit 1
fi
aws s3 cp startup.sh "s3://${BUCKET_NAME}/startup.sh"
echo -e "${GREEN}✓ startup.sh uploaded${NC}"
echo ""

# Upload plugins.zip
echo -e "${YELLOW}[5/5]${NC} Uploading plugins.zip..."
if [ ! -f "plugins.zip" ]; then
    echo -e "${YELLOW}WARNING: plugins.zip not found, skipping...${NC}"
else
    aws s3 cp plugins.zip "s3://${BUCKET_NAME}/plugins/plugins.zip"
    echo -e "${GREEN}✓ plugins.zip uploaded${NC}"
fi
echo ""

# Verify uploads
echo -e "${YELLOW}Verifying uploaded files...${NC}"
echo -e "Files in S3 bucket:"
aws s3 ls "s3://${BUCKET_NAME}/" --recursive | grep -E "(requirements.txt|startup.sh|plugins.zip|dags/)"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Pre-deployment completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "You can now deploy the CloudFormation stack:"
echo -e "${YELLOW}aws cloudformation deploy --template-file template.yaml --stack-name ${ENV}-mwaa --parameter-overrides Env=${ENV}${NC}"
echo ""
