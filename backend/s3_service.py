import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def upload_file_to_s3(file_content, filename):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=file_content
    )

    return f"s3://{BUCKET_NAME}/{filename}"

def download_file_from_s3(filename):
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=filename
    )

    return response["Body"].read()