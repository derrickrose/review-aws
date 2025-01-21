from typing import Optional


PROFILE = "default"


def get_profile(line: str) -> Optional[str]:
    import re
    pattern = "^\\[.+\\]$"
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


import s3fs

cred = credentials()[PROFILE]
print(cred)
fs = s3fs.S3FileSystem(
    key=cred["aws_access_key_id"],
    secret=cred["aws_secret_access_key"],
    use_ssl=False
)
bucket = "dev-eu-west-3-frils-s3fs"

import pyarrow.dataset as ds
from pyarrow import Table

arrow_table: Table = ds.dataset(
    bucket,
    filesystem=fs,
    format="parquet"
).to_table()
pandas_dataframe = arrow_table.to_pandas()
print(pandas_dataframe)
