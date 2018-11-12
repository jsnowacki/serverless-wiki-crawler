import boto3
import json
import logging
import wiki
import os

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

s3_content_type = os.environ.get('S3_CONTENT_TYPE', 'text/plain')
s3_bucket_name = os.environ['S3_BUCKET_NAME']

s3 = boto3.resource('s3')
s3_bucket = s3.Bucket(s3_bucket_name)

dynamodb_table_name = os.environ['DYBAMODB_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')

dynamodb_table = dynamodb.Table(dynamodb_table_name)

def wiki_crawler(event, context):
    logger.debug('Event: {}'.format(event))

    lang = event.get('lang')
    logger.debug('Lang: {}'.format(lang))

    content = wiki.parse_main(lang)
    logger.debug('Content: {}'.format(content))

    if content is None or content == {}:
        logger.warn('Nothing crawled for wikipedia language {}'.format(lang))
        return

    object_name = 'wikipedia-{lang}-{title}-{timestamp}.json'.format(**content).replace(' ', '_')
    body = json.dumps(content)
    s3.Bucket(s3_bucket_name).put_object(Key=object_name, Body=body, ContentType=s3_content_type)
    logger.info('File {}/{} uploaded'.format(s3_bucket_name, object_name))

    dynamodb_table.put_item(Item=content)
    logger.info('Item put into table {}: {}'.format(dynamodb_table_name, content))
