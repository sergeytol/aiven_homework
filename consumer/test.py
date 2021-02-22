import os
import datetime
import time

import psycopg2
import psycopg2.extras
from psycopg2 import Error

from .main import insert_metrics_to_db


def test_insert_metrics_to_db():
    """Test for insert_metrics_to_db"""

    # test data

    messages = [
        {
            'successful': True,
            'url': 'https://google.com/',
            'checked_at': '2021-02-21T12:36:36.158846',
            'metrics': {'status_code': 200, 'request_time': 0.6240579410077771, 'pattern_match': True}
        },
        {
            'successful': True,
            'url': 'https://sergeytolokonnikov.rocks/',
            'checked_at': '2021-02-21T12:36:36.161400',
            'metrics': {'status_code': 200, 'request_time': 0.33387805901293177, 'pattern_match': False}
        },
        {
            'successful': False,
            'url': 'https://desdjsejdsiejfsefjsoisejfioesfjo.site/',
            'checked_at': '2021-02-21T12:36:36.161766',
            'error_message': 'Cannot connect to host desdjsejdsiejfsefjsoisejfioesfjo.site:443 '
                             'ssl:default [Name or service not known]'
        }
    ]

    # expected data

    expected = [
        {
            'url': 'https://google.com/',
            'successful': True,
            'status_code': 200,
            'pattern_match': True,
            'error_message': None
        },
        {
            'url': 'https://sergeytolokonnikov.rocks/',
            'successful': True,
            'status_code': 200,
            'pattern_match': False,
            'error_message': None
        },
        {
            'url': 'https://desdjsejdsiejfsefjsoisejfioesfjo.site/',
            'successful': False,
            'status_code': None,
            'requestTime': None,
            'pattern_match': None,
            'error_message': 'Cannot connect to host desdjsejdsiejfsefjsoisejfioesfjo.site:443 '
                             'ssl:default [Name or service not known]'
        }
    ]

    # connect to DB, try to reconnect if DB isn't ready yet

    attempt = 1
    reconnect_attempts_count = int(os.getenv('TESTING_RECONNECT_ATTEMPTS_COUNT'))
    reconnect_timeout = float(os.getenv('TESTING_RECONNECT_TIMEOUT_SEC'))
    while attempt < reconnect_attempts_count:
        try:
            db_connection = psycopg2.connect(user=os.getenv('TEST_POSTGRES_USER'),
                                             password=os.getenv('TEST_POSTGRES_PASSWORD'),
                                             host=os.getenv('TEST_POSTGRES_HOST'),
                                             port=os.getenv('TEST_POSTGRES_PORT'),
                                             database=os.getenv('TEST_POSTGRES_DB'))
            break
        except Error:
            print(f'Unable to connect to the testing database (attempt {attempt} from {reconnect_attempts_count}). '
                  f'Maybe schema is not completely restored from dump yet, '
                  f'so trying to reconnect in {reconnect_timeout} sec')
            time.sleep(reconnect_timeout)
            attempt += 1

    # check every message in the test dataset

    try:
        for index, message in enumerate(messages):

            inserted_id = insert_metrics_to_db(message, db_connection)
            db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                db_cursor.execute("select * from website_check_result where id = %s", (inserted_id,))
                row = db_cursor.fetchone()
            finally:
                if db_cursor:
                    db_cursor.close()
            for key in row.keys():
                if key in expected[index]:
                    assert expected[index][key] == row[key]
                    if key == 'checked_at':
                        assert isinstance(row[key], datetime)
                        assert messages[index][key] == row[key].isoformat()
    finally:
        if db_connection:
            db_connection.close()
