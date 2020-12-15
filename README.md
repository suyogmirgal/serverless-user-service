# Serverless User Service

- This is Sample Serverless user Project with Circle ci configuration


## Local Environment:

## Dynamo DB:

Web Console: http://localhost:8000/shell/

#### DynamoDB JavaScript Shell
List all tables:

```
dynamodb.listTables(function(err, data) {
    if (err) ppJson(err); 
    else ppJson(data); 
});
```

Scan table:

```
var params = {
    TableName: 'local-userDetails'
};
dynamodb.scan(params, function(err, data) {
    if (err) ppJson(err); 
    else ppJson(data);
});
```

Scan table by email:

```
var input_email = 'test_api_user1@mail.com';
var params = {
    TableName: 'local-userDetails',
    FilterExpression: '#email = :value',
    ExpressionAttributeNames: { 
        '#email' : 'email'
    },
     ExpressionAttributeValues: {   
        ':value' : {'S' : input_email}
    }
};
dynamodb.scan(params, function(err, data) {
    if (err) ppJson(err); 
    else ppJson(data);
});
```

## SQS:

Push message in default SQS:

```
aws --endpoint-url http://localhost:9324 sqs send-message --queue-url http://localhost:9324/queue/default --message-body "{\"first_name\": \"Suyog\", \"last_name\": \"M\", \"email\": \"suyog@mail.com\", \"dob\": \"2000-11-11\"}"

```

Push message in default local-userInputSQS:

```
aws --endpoint-url http://localhost:9324 sqs send-message --queue-url http://localhost:9324/queue/local-userInputSQS --message-body "{\"first_name\": \"Suyog\", \"last_name\": \"M\", \"email\": \"suyog@mail.com\", \"dob\": \"2000-11-11\"}"

```
