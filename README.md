# Serverless User Service

- This is Sample Serverless user Project with Circle ci configuration


##Local Environment:

##Dynamo DB:

Web Console: http://localhost:8000/shell/

####DynamoDB JavaScript Shell
List all tables:

```
dynamodb.listTables(function(err, data) {
    if (err) ppJson(err); 
    else ppJson(data); 
});
```


```
var params = {
    TableName: 'table_name',
    FilterExpression: 'attribute_name = :value'
};
dynamodb.scan(params, function(err, data) {
    if (err) ppJson(err); 
    else ppJson(data);
});
```

