import boto3

session = boto3.Session(aws_access_key_id='ACCESS_KEY',
                        aws_secret_access_key='SECRET_KEY')
s3 = session.resource('s3')
output_appflow = s3.Bucket('output-appflow')

print("bucket inside miaradia ----------------------------------------------------------------------")
for my_bucket_object in output_appflow.objects.all():
    print(my_bucket_object.key)

client = session.client('sts')
assumed_role_object = client.assume_role(
    RoleArn="arn:aws:iam::893739846413:role/MiaradiaS3FullAccess",
    RoleSessionName="MiaradiaS3FullAccess"
)
credentials = assumed_role_object['Credentials']

session = boto3.Session(aws_access_key_id=credentials['AccessKeyId'],
                        aws_secret_access_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken'])

s3_resource = session.resource(
    's3')

print("bucket inside izy be account --------------------------------------------------------------")
for bucket in s3_resource.buckets.all():
    print(bucket.name)
