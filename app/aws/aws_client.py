import os
import boto3

class AwsClient:
    def __int__(self):
        self.ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID', '')
        self.SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY', '')

    def s3_client(self):
        return boto3.client('s3', aws_access_key_id=self.ACCESS_KEY_ID, aws_secret_access_key=self.SECRET_ACCESS_KEY)

    def sqs_client(self):
        pass