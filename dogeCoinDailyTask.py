from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import re

from twitter import Twitter
from doge import Doge
sched = BlockingScheduler()
q = Queue(connection=conn)


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    q = Queue(connection=conn)
    print(q.enqueue(Twitter().run))
    print(q.enqueue(Doge().run))
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    q = Queue(connection=conn)
    q.enqueue(Twitter().run)
    q.enqueue(Doge().run)
    print('This job is run every weekday at 5pm.')

sched.start()
