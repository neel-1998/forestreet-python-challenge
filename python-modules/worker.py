from os import environ
import redis
from rq import Worker, Connection

# Setup variables and read environment variables
redis_url = environ.get("REDIS_URL", "redis://localhost:6379")
queue_name = environ.get("QUEUE_NAME", "word-count-queue")

# Setup Redis connection
redis_conn = redis.from_url(redis_url)

# Setup worker to be active on module execution
if __name__ == "__main__":
    try:
        with Connection(redis_conn):
            worker = Worker(queue_name)
            worker.work()
    except:
        print("Redis connection failed")