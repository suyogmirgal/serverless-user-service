import json
from src.service import dynamo


def create_user(event, context):
    user_data = json.loads(event["Records"][0]["body"])
    dynamo.create_user(user_data=user_data)
    print(f"User {user_data.get('email')} from SQS created")
    return {"statusCode": 200, "body": json.dumps({"Message": "User Created"})}
