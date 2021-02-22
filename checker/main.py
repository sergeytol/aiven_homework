#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import re
from datetime import datetime
from distutils.util import strtobool
from time import sleep
from timeit import default_timer

import aiohttp
from aiohttp import ClientSession, ClientConnectionError, ClientError
from kafka import KafkaProducer


def get_websites_list(path_to_file: str) -> list:
    """Reads a websites list from file"""
    with open(path_to_file, encoding='utf-8') as file:
        return json.loads(file.read())


async def request(session: ClientSession, url: str) -> dict:
    """Make an async request"""
    start_time = default_timer()
    async with session.get(url) as response:
        request_time = default_timer() - start_time
        return {
            'status_code': response.status,
            'request_time': request_time,
            'response_text': await response.text()
        }


async def build_metrics(session: ClientSession, url: str) -> dict:
    """Build metrics for a request"""
    data = {
        'successful': True,
        'url': url,
        'checked_at': datetime.utcnow().isoformat()
    }
    try:
        response = await request(session, url)
        data['metrics'] = response
    except ClientError as error:
        data['successful'] = False
        data['error_message'] = f'{error}'

    return data


async def request_all(urls: list, event_loop: asyncio.BaseEventLoop) -> list:
    """Bulk async request"""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        return await asyncio.gather(*[build_metrics(session, url) for url in urls],
                                    return_exceptions=True)


def get_raw_metrics(websites: dict) -> list:
    """Get raw websites metrics"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(request_all([x['url'] for x in websites], loop))


def process_metrics(metrics: list, websites: list) -> list:
    """Final metrics preparation / postprocessing"""

    def func(data):
        i, item = data
        if item['successful']:
            if item['url'] == websites[i]['url'] and 'pattern' in websites[i]:
                item['metrics']['pattern_match'] = \
                    bool(re.search(websites[i]['pattern'], item['metrics']['response_text']))
            del item['metrics']['response_text']
        return item

    return list(map(func, enumerate(metrics)))


if __name__ == '__main__':

    dev_env = strtobool(os.getenv('DEV_ENV'))

    # setup logger

    logger = logging.getLogger('checker')
    log_level = logging.DEBUG if dev_env else logging.INFO
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    file_handler = logging.FileHandler(os.getenv('CHECKER_LOG_FILE'))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.debug('Hello, Checker!')

    # read websites list

    try:
        websites_list = get_websites_list(os.getenv('WEBSITES_LIST_FILE'))
    except Exception as exc:
        logger.critical(f'Error! Unable to get a websites list: {exc}')
        exit(1)

    # main loop

    while True:

        # get metrics

        try:
            results = get_raw_metrics(websites_list)
            processed_results = process_metrics(results, websites_list)
        except Exception as exc:
            logger.critical(f'Error! Unable to get metrics for the websites list: {exc}')
            exit(1)

        # send metrics to Kafka

        try:
            producer = KafkaProducer(
                value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                bootstrap_servers=[os.getenv('KAFKA_BROKERCONNECT')],
                security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL') if not dev_env else 'PLAINTEXT',
                sasl_plain_username=os.getenv('KAFKA_SASL_PLAIN_USERNAME') if not dev_env else None,
                sasl_plain_password=os.getenv('KAFKA_SASL_PLAIN_PASSWORD') if not dev_env else None,
                ssl_cafile=os.getenv('KAFKA_SSL_CAFILE') if not dev_env else None,
                sasl_mechanism=os.getenv('KAFKA_SASL_MECHANISM') if not dev_env else None
            )
        except Exception as exc:
            logger.critical(f'Error! Unable to connect to Kafka: {exc}')
            exit(1)

        # send results to kafka topic

        try:
            for result in processed_results:
                if not isinstance(result, ClientConnectionError):
                    producer.send(os.getenv('KAFKA_TOPIC'), result)
                    logger.info(f'Sent: {result}')
        except Exception as exc:
            logger.error(f'Error! Unable to send the message to Kafka: {exc}')

        # sleep until the next checking

        sleep(float(os.getenv('CHECKER_TIMEOUT_SEC')))
