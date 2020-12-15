from pytest_bdd import scenario, given, when, then
import requests
import pytest
import json
import boto3
import time
from boto3.dynamodb.conditions import Attr

USER_SERVICE_BASE_URL = "http://localhost:3000"
ENV = "local"
DYNAMO_ENDPOINT_URL = "http://localhost:8000"
DYNAMO_LOCAL_USER_TABLE = "local-userDetails"
SQS_ENDPOINT_URL = "http://localhost:9324/queue"
USER_INPUT_SQS_URL = "http://localhost:9324/queue/local-userInputSQS"


@pytest.fixture(scope="function")
def context():
    return {}


@scenario(
    "user_service.feature", "successful user registration from /user POST API request"
)
def test_successful_user_registration(context):
    pass


@given("user service up and running")
def user_service_running(context):
    health_response = requests.get(f"{USER_SERVICE_BASE_URL}/{ENV}/user-service/health")
    assert health_response.status_code == 200


@when("POST /user request with valid user details made")
def create_user_by_api_request(context):
    user_data = {
        "first_name": "test",
        "last_name": "user",
        "email": "test_user@mail.com",
        "dob": "2000-03-01",
    }
    headers = {"Content-Type": "application/json"}

    context["create_user_response"] = requests.post(
        f"{USER_SERVICE_BASE_URL}/{ENV}/user",
        headers=headers,
        data=json.dumps(user_data),
    )


@then("user is successfully registered in System")
def verify_user_created_by_api_request(context):
    # verify POST /user API status code and response body
    assert context["create_user_response"].status_code == 200
    assert (
        json.loads(context["create_user_response"].text).get("Message")
        == "User Created"
    )

    # verify user details created in userDetail dynamoDB table
    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMO_ENDPOINT_URL)
    user_table = dynamodb.Table(DYNAMO_LOCAL_USER_TABLE)
    search_result = user_table.scan(
        FilterExpression=Attr("email").eq("test_user@mail.com")
    )

    assert len(search_result["Items"]) > 0
    user = search_result["Items"][0]
    assert user["firstName"] == "test"
    assert user["lastName"] == "user"
    assert user["dob"] == "2000-03-01"


@scenario(
    "user_service.feature", "successful user registrations from /user POST API request"
)
def test_successful_user_registrations(context):
    pass


@when(
    "POST /user request with Email as <email>, First name as <first_name>, Last name as <last_name> and DOB as <dob> "
    "is made"
)
def create_user_by_api_request_with_given_user_details(
    context, email, first_name, last_name, dob
):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "dob": dob,
    }
    headers = {"Content-Type": "application/json"}

    context["create_user_response"] = requests.post(
        f"{USER_SERVICE_BASE_URL}/{ENV}/user",
        headers=headers,
        data=json.dumps(user_data),
    )


@then(
    "user is successfully registered with Email as <email>, First name as <first_name>, Last name as <last_name> and"
    " DOB as <dob>"
)
def verify_user_created_by_api_request_for_given_user_details(
    context, email, first_name, last_name, dob
):
    # verify POST /user API status code and response body
    assert context["create_user_response"].status_code == 200
    assert (
        json.loads(context["create_user_response"].text).get("Message")
        == "User Created"
    )

    # verify user details created in userDetail dynamoDB table
    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMO_ENDPOINT_URL)
    user_table = dynamodb.Table(DYNAMO_LOCAL_USER_TABLE)
    search_result = user_table.scan(FilterExpression=Attr("email").eq(email))

    assert len(search_result["Items"]) > 0
    user = search_result["Items"][0]
    assert user["firstName"] == first_name
    assert user["lastName"] == last_name
    assert user["dob"] == dob


@scenario("user_service.feature", "successful user creation from userInputSQS")
def test_successful_user_creation_from_sqs(context):
    pass


@when(
    "message received in userInputSQS with Email as <email>, First name as <first_name>, Last name as <last_name> and"
    " DOB as <dob> is made"
)
def push_message_to_user_input_sqs(email, first_name, last_name, dob):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "dob": dob,
    }
    sqs = boto3.client("sqs", endpoint_url=SQS_ENDPOINT_URL)
    sqs.send_message(QueueUrl=USER_INPUT_SQS_URL, MessageBody=(json.dumps(user_data)))


@then(
    "user is successfully created with Email as <email>, First name as <first_name>, Last name as <last_name> and DOB "
    "as <dob>"
)
def verify_user_created_from_user_input_sqs(email, first_name, last_name, dob):
    # verify user details created in userDetail dynamoDB table
    counter = 0
    while True:
        dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMO_ENDPOINT_URL)
        user_table = dynamodb.Table(DYNAMO_LOCAL_USER_TABLE)
        search_result = user_table.scan(FilterExpression=Attr("email").eq(email))

        if len(search_result["Items"]) == 0 and counter < 10:
            time.sleep(1)
            counter += 1
            continue
        elif len(search_result["Items"]) > 0:
            user = search_result["Items"][0]
            assert user["firstName"] == first_name
            assert user["lastName"] == last_name
            assert user["dob"] == dob
            break
        elif counter == 10:
            assert False, f"User {email} from SQS is not created"
