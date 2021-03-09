from os import environ
from flask import Flask
import redis
from rq import Queue, Connection
from rq.job import Job
import rq.exceptions

import tasks

# Create the Flask instance
app = Flask(__name__)

# Setup variables and read environment variables
redis_host = environ.get("REDIS_HOST", "localhost")
redis_port = int(environ.get("REDIS_PORT", 6379))
queue_name = environ.get("QUEUE_NAME", "word-count-queue")
result_ttl = int(environ.get("RESULT_TTL", 60))
request_ttl = int(environ.get("REQUEST_TTL", 60))
web_server_host = environ.get("WEB_SERVER_HOST", "localhost")
web_server_port = int(environ.get("WEB_SERVER_PORT", 5000))

# Setup Redis connection
redis_url = f"redis://{redis_host}:{redis_port}"
redis_conn = redis.from_url(redis_url)

@app.route("/", methods=["GET"])
def index():
    response = """
        Welcome to the index page.
        </br>
        </br>
        This webserver can return the number of words of any sentence. Try it out by entering a sentence after the '/' using the POST method.
        </br>
        </br>
        Note any collection of characters (excluding spaces) with a space on either side will be considered a word.
    """
    return response

@app.route("/<req_str>", methods=["POST"])
def queue_word_count(req_str):
    with Connection(redis_conn):
        q = Queue(queue_name)
        job = q.enqueue(
            tasks.word_counter,
            req_str,
            result_ttl=result_ttl,
            ttl=request_ttl
        )
    job_id = job.get_id()
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
    return response

@app.route("/job/<job_id>", methods=["GET"])
def get_word_count(job_id):
    try:
        with Connection(redis_conn):
            job = Job.fetch(job_id)
    except rq.exceptions.NoSuchJobError as e:
        return "This job does not exist", 404
    except:
        return "Redis connection error"

    if job.is_finished:
        return f"The sentence {job.args[0]} has {job.result} words"
    else:
        status = job.get_status()
        return f"This job has status: {status}", 202

if __name__ == "__main__":
    app.run(host=web_server_host, port=web_server_port)