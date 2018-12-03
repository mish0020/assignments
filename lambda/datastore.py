import base64
import json

import boto3
import os


def db_writer(event, context):

    item = None
    dynamo_db = boto3.resource('dynamodb')

    table_arn = os.environ['TABLE_NAME']
    arn,table_name = table_arn.split("/",1)
    table = dynamo_db.Table(table_name)

    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]

    with table.batch_writer() as batch_writer:
       for item in deserialized_data:
          batch_writer.put_item(Item=item)
