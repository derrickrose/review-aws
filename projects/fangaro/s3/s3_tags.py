import os
from typing import Optional

import boto3

PROFILE = "default"


def get_profile(line: str) -> Optional[str]:
    import re
    pattern = "^\[.+\]$"
    result = re.search(pattern, line.strip())
    return result.group().replace("[", "").replace("]", "") if result else None


def get_access_key(line: str) -> Optional[str]:
    if line.__contains__("aws_access_key_id"):
        access_key = line.replace(" ", "").strip().split("aws_access_key_id=")[1].split("'")[0]
        return access_key if access_key else None
    return None


def get_secret_key(line: str) -> Optional[str]:
    if line.__contains__("aws_secret_access_key"):
        secret_key = line.replace(" ", "").strip().split("aws_secret_access_key=")[1].split("'")[0]
        return secret_key if secret_key else None
    return None


def credentials(credentials_path: str = "/home/frils/.aws/credentials") -> dict[str, dict[str, str]]:
    with open(credentials_path, "r") as f:
        credentials_map: dict = {}
        current_profile: str = ""
        current_credential: dict = {}
        for line in f.readlines():
            profile = get_profile(line)
            if profile:
                current_profile = profile

            access_key = get_access_key(line)
            if access_key:
                current_credential["aws_access_key_id"] = access_key
            else:
                secret_key = get_secret_key(line)
                if secret_key:
                    current_credential["aws_secret_access_key"] = secret_key
                    credentials_map[current_profile] = current_credential.copy()
                    current_credential = {}
                    current_profile = ""
    return credentials_map


def get_s3_object_tags(bucket_name, key):
    creds = credentials()[PROFILE]
    s3 = boto3.client('s3',
                      aws_access_key_id=creds["aws_access_key_id"],
                      aws_secret_access_key=creds["aws_secret_access_key"])

    response = s3.get_object_tagging(Bucket=bucket_name, Key=key)
    print(str(response).replace("'", '"'))

    tags = response.get('TagSet', [])
    return tags


def put_s3_object_tag(bucket, key, tag_key, tag_value):
    s3 = boto3.client('s3')

    # Define the tag dictionary
    tag_dict = {
        'TagSet': [
            {
                'Key': tag_key,
                'Value': tag_value
            },
        ]
    }

    # Put the tag on the s3 object
    response = s3.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging=tag_dict
    )

    return response



put_s3_object_tag('output-appflow', 'folder/rcookbook2e.pdf', 'title', 'mami')


tags = get_s3_object_tags('output-appflow', 'folder/rcookbook2e.pdf')
for tag in tags:
    print(f"Key: {tag['Key']}, Value: {tag['Value']}")
