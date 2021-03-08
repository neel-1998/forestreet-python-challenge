# forestreet-python-challenge

## Functional Spec
Create a system that will count the number of words in a sentence using a worker and a job queue. There should be two services. One that receives the request and a worker that computes the answer.
The user should be able to:

- Post a sentence to an endpoint
- Get back the number of words

## Solution
### General
My solution to this task uses 3 services:
1. A web server/job queue (`request-handler.py`)
2. A worker (`worker.py`)
3. A Redis server

### Requirements
It is assumed that `Docker` (version >= 20.10.5) and `docker-compose` (version >= 1.28.5) are installed.
### Usage
1. Clone this repo
2. Run the command to start all services:

        docker-compose up
    If you would like to run these services in the background then use:

        docker-compose up -d
3. Go to http://localhost:5000 and follow the on-screen instruction
4. Once finished, stop all services using:

        ^C

    or to stop background services use:

        docker-compose stop

5. Clean-up all containers [and images] using:

        docker-compose down [--rmi all]

### Configuration
There are a handful of environment variables the Python modules will attempt to retrieve. These can be defined in the `docker-compose.yml`. They have all been given default values for out of the box use.

For `request-handler.py`:

        REDIS_URL - URL to connect to Redis server (default = "redis://localhost:6379")
        QUEUE_NAME - Name of the Queue (default = "word-count-queue")
        RESULT_TTL - Time to live for the result (default = 60)
        REQUEST_TTL - Time to live for the request in the queue (default = 60)
        WEB_SERVER_HOST - IP address the web server will be operating on (default = "localhost")
        WEB_SERVER_PORT - Port the web server will be operating on (default = 5000)

For `worker.py`:

        REDIS_URL - URL to connect to Redis server (default = "redis://localhost:6379")
        QUEUE_NAME - Name of the Queue (default = "word-count-queue")

### Notes
- Manual testing has been done - would like to implement automated testing.
- Redundant files on web-queue and worker services - I create one docker image which contains all python modules. Each service should only need the python module called (and module imports), leaving at least one unused file on each service. I did this because it seemed more efficient than building 2 images which would use more storage. Workaround could involve using volumes in the `docker-compose.yml`.
- Could implement some logging to help debug.