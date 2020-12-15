import boto3
import os
import uuid


def create_user(user_data):
    dynamo_client().put_item(
        TableName=os.getenv("USER_TABLE"),
        Item={
            "id": {"S": str(uuid.uuid4())},
            "email": {"S": user_data.get("email")},
            "firstName": {"S": user_data.get("first_name")},
            "lastName": {"S": user_data.get("last_name")},
            "dob": {"S": user_data.get("dob")},
        },
    )


def dynamo_client():
    if os.getenv("IS_OFFLINE") == "true":
        return boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    return boto3.client("dynamodb")
