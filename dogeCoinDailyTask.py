"""Schedules collection of tweets and doge prices.

Schedules to collect tweets and doge coin prices daily.
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import re
from twitter import Twitter
from doge import Doge

sched = BlockingScheduler()
q = Queue(connection=conn)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    q = Queue(connection=conn)
    q.enqueue(Twitter().run)
    q.enqueue(Doge().run)
    print('This job is run every weekday at 5pm.')

sched.start()


if __name__ == "__main__":
    sched.start()
