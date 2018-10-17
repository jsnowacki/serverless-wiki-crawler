import boto3
import json
import logging
import wiki

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def wiki_crawler(event, context):
    logger.debug('Event: {}'.format(event))

    lang = event.get('lang')
    logger.debug('Lang: {}'.format(lang))

    content = wiki.parse_main(lang)
    logger.debug('Content: {}'.format(content))

