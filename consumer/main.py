#!/usr/bin/env python3
import logging
from distutils.util import strtobool
import json
import os
from time import sleep

import psycopg2
from kafka import KafkaConsumer
from psycopg2 import Error


def insert_metrics_to_db(data: dict, db_connection) -> int:
    """Inserts metrics data to the database"""
    db_cursor = db_connection.cursor()

    # prepare some metrics
    status_code = data['metrics']['status_code'] \
        if data['successful'] and 'status_code' in data['metrics'] else None
    request_time = data['metrics']['request_time'] \
        if data['successful'] and 'request_time' in data['metrics'] else None
    pattern_match = data['metrics']['pattern_match'] \
        if data['successful'] and 'pattern_match' in data['metrics'] else None

    try:
        db_cursor.execute(
            """insert into website_check_result
               (url, successful, status_code, request_time, pattern_match, checked_at, error_message)
               values (%s, %s, %s, %s, %s, %s, %s) returning id""",
            (
                data['url'],
                data['successful'],
                status_code,
                request_time,
                pattern_match,
                data['checked_at'],
                data['error_message'] if 'error_message' in data else None
            )
        )
        db_connection.commit()
        row_id = db_cursor.fetchone()[0]
    finally:
        if db_cursor:
            db_cursor.close()

    return row_id


if __name__ == '__main__':

    dev_env = strtobool(os.getenv('DEV_ENV'))

    # setup logger

    logger = logging.getLogger('consumer')
    log_level = logging.DEBUG if dev_env else logging.INFO
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    file_handler = logging.FileHandler(os.getenv('CONSUMER_LOG_FILE'))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.debug('Hello, Consumer!')

    # connect to Kafka

    try:
        consumer = KafkaConsumer(
            os.getenv('KAFKA_TOPIC'),
            value_deserializer=lambda m: json.loads(m),
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

    # crate DB connection

    try:
        db_connection = psycopg2.connect(user=os.getenv('POSTGRES_USER'),
                                         password=os.getenv('POSTGRES_PASSWORD'),
                                         host=os.getenv('POSTGRES_HOST'),
                                         port=os.getenv('POSTGRES_PORT'),
                                         database=os.getenv('POSTGRES_DB'))
    except (Exception, Error) as exc:
        logger.critical(f'Error! Unable to connect to database: {exc}')
        exit(1)

    # main loop

    try:
        while True:
            for message in consumer:
                logger.info(f'Received: {message.value}')

                # write metrics to DB

                try:
                    inserted_id = insert_metrics_to_db(message.value, db_connection)
                    logger.info(f"Inserted with ID {inserted_id}: {message.value}")
                except (Exception, Error) as exc:
                    logger.error("Error while working with database: ", exc)

            sleep(float(os.getenv('CONSUMER_TIMEOUT_SEC')))
    finally:
        if db_connection:
            db_connection.close()
            logger.info("Database connection closed")
