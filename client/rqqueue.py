from redis import Redis
from rq import Queue

queue =Queue(connection=Redis(
     port="6379",
    host="localhost"
))
