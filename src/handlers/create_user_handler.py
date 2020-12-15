import json
from src.service import dynamo


def create_user(event, context):
    user_data = json.loads(event["body"])
    dynamo.create_user(user_data=user_data)
    return {"statusCode": 200, "body": json.dumps({"Message": "User Created"})}
