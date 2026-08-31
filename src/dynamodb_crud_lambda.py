"""
LambdaFunctionOverHttps
------------------------
Backs the POST /DynamoDBManager resource in API Gateway.

Supports basic CRUD + list operations against a DynamoDB table.
"""

from __future__ import print_function
import boto3
import json

print('Loading function')


def lambda_handler(event, context):
    """
    Expected event shape:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: parameters passed to the operation being performed
    """
    operation = event['operation']

    if 'tableName' in event:
        dynamo = boto3.resource('dynamodb').Table(event['tableName'])

    operations = {
        'create': lambda x: dynamo.put_item(**x),
        'read': lambda x: dynamo.get_item(**x),
        'update': lambda x: dynamo.update_item(**x),
        'delete': lambda x: dynamo.delete_item(**x),
        'list': lambda x: dynamo.scan(**x),
        'echo': lambda x: x,
        'ping': lambda x: 'pong'
    }

    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))
