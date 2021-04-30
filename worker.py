""" Worker to run tasks using redis.

Started via Procfile entry which is used by Heroku to start a process for this file.
Process queue filled by the Scheduler in dogeCoinDailyTasks.py.
"""
import os
import re
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()