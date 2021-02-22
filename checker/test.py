import asyncio
from datetime import datetime
import os
import re

import dateutil.parser

from .main import get_websites_list, request_all, get_raw_metrics, process_metrics


def test_get_websites_list():
    """Test for get_websites_list function"""
    try:
        get_websites_list('wrong')
    except Exception as e:
        assert isinstance(e, FileNotFoundError)

    result = get_websites_list(os.getenv('WEBSITES_LIST_FILE'))

    assert isinstance(result, list)
    assert 'pattern' in result[0]
    assert 'url' in result[0]


def test_request_all():
    """Test for request_all function"""
    websites = get_websites_list(os.getenv('WEBSITES_LIST_FILE'))
    loop = asyncio.get_event_loop()

    results = loop.run_until_complete(request_all([x['url'] for x in websites], loop))

    assert isinstance(results, list)

    for index in [0, 1]:

        assert isinstance(results[index], dict)
        assert 'checked_at' in results[index]
        assert isinstance(dateutil.parser.parse(results[0]['checked_at']), datetime)
        assert 'metrics' in results[index]
        assert isinstance(results[index]['metrics'], dict)
        assert 'url' in results[index]
        assert results[index]['url'] == websites[index]['url']
        assert 'successful' in results[index]
        assert results[index]['successful'] == True
        assert 'status_code' in results[index]['metrics']
        assert 'request_time' in results[index]['metrics']
        assert 'response_text' in results[index]['metrics']
        assert results[index]['metrics']['status_code'] == 200
        assert isinstance(results[index]['metrics']['request_time'], float)
        assert isinstance(results[index]['metrics']['response_text'], str)
        assert re.search('html', results[index]['metrics']['response_text'])

    assert isinstance(results[2], dict)
    assert 'url' in results[2]
    assert results[2]['url'] == websites[2]['url']
    assert 'status_code' not in results[2]
    assert 'metrics' not in results[2]
    assert 'successful' in results[2]
    assert results[2]['successful'] == False
    assert 'error_message' in results[2]
    assert isinstance(results[2]['error_message'], str)
    assert re.search('Cannot connect to host', results[2]['error_message'])


def test_process_metrics():
    """Test for process_metrics function"""
    websites_list = get_websites_list(os.getenv('WEBSITES_LIST_FILE'))
    raw_results = get_raw_metrics(websites_list)
    results = process_metrics(raw_results, websites_list)

    assert isinstance(results, list)
    assert isinstance(results[0], dict)

    for index in [0, 1]:

        assert 'pattern_match' in results[index]['metrics']
        assert results[index]['metrics']['pattern_match'] == (index == 0)
        assert 'response_text' not in results[0]['metrics']
