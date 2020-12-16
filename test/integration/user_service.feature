Feature: User Service

    Scenario: successful user registration from /user POST API request
        Given user service up and running
        When POST /user request with valid user details made
        Then user is successfully registered in System

    Scenario Outline: successful user registrations from /user POST API request
        Given user service up and running
        When POST /user request with Email as <email>, First name as <first_name>, Last name as <last_name> and DOB as <dob> is made
        Then user is successfully registered with Email as <email>, First name as <first_name>, Last name as <last_name> and DOB as <dob>
        Examples:
        | email                   | first_name  | last_name | dob        |
        | test_api_user1@mail.com | test1       | api_user1 | 2012-01-01 |
        | test_api_user2@mail.com | test2       | api_user2 | 2012-01-02 |

    Scenario Outline: successful user creation from userInputSQS
        Given user service up and running
        When message received in userInputSQS with Email as <email>, First name as <first_name>, Last name as <last_name> and DOB as <dob>
        Then user is successfully created with Email as <email>, First name as <first_name>, Last name as <last_name> and DOB as <dob>
        Examples:
        | email                   | first_name  | last_name | dob        |
        | test_api_sqs1@mail.com | test1       | sqs_user1 | 2012-01-03 |
        | test_api_sqs2@mail.com | test2       | sqs_user2 | 2012-01-04 |