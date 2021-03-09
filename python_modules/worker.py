from os import environ
import redis
from rq import Worker, Connection

# Setup variables and read environment variables
redis_host = environ.get("REDIS_HOST", "localhost")
redis_port = int(environ.get("REDIS_PORT", 6379))
queue_name = environ.get("QUEUE_NAME", "word-count-queue")

# Setup Redis connection
redis_url = f"redis://{redis_host}:{redis_port}"
redis_conn = redis.from_url(redis_url)

def start_worker():
    try:
        with Connection(redis_conn):
            worker = Worker(queue_name)
            worker.work()
    except:
        print("Redis connection failed")

# Setup worker to be active on module execution
if __name__ == "__main__":
    start_worker()