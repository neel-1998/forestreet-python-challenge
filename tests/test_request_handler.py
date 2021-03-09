from os import environ
import pytest
from python_modules import request_handler, worker
from mock import patch
from rq import Queue, SimpleWorker
from fakeredis import FakeStrictRedis
import time

redis_host = environ.get("REDIS_HOST", "localhost")
redis_port = int(environ.get("REDIS_PORT", 6379))
result_ttl = int(environ.get("RESULT_TTL", 60))
request_ttl = int(environ.get("REQUEST_TTL", 60))
web_server_host = environ.get("WEB_SERVER_HOST", "localhost")
web_server_port = int(environ.get("WEB_SERVER_PORT", 5000))

@pytest.fixture
def app():
    yield request_handler.app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    expected = b"""
        Welcome to the index page.
        </br>
        </br>
        This webserver can return the number of words of any sentence. Try it out by entering a sentence after the '/' using the POST method.
        </br>
        </br>
        Note any collection of characters (excluding spaces) with a space on either side will be considered a word.
    """
    assert expected == res.get_data()

@patch("python_modules.request_handler.redis_conn", FakeStrictRedis(host=redis_host, port=redis_port))
def test_queue_word_count(client):
    res = client.post("/this is a test sentence")
    assert res.status_code == 200
    job_id = res.get_data().split()[0].decode("utf-8")
    response = f"""
        {job_id}
        </br>
        </br>
        Your request has now been added to a job queue with a ttl of {request_ttl}s.
        </br>
        </br>
        To see the status/outcome of you job, make a GET request to /job/{job_id}
        </br>
        </br>
        Your result ttl is {result_ttl}s.
    """
    expected = bytes(response, "utf-8")
    assert expected == res.get_data()

@patch("python_modules.request_handler.redis_conn", FakeStrictRedis(host=redis_host, port=redis_port))
def test_get_word_count_no_worker(client):
    res_post = client.post("/this is a test sentence")
    assert res_post.status_code == 200

    job_id = res_post.get_data().split()[0].decode("utf-8")
    res_get = client.get(f"/job/{job_id}")
    assert res_get.status_code == 202
    expected = b"This job has status: queued"
    assert expected == res_get.get_data()
