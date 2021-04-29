from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn

q = Queue(connection=conn)

from twitter import Twitter
from doge import Doge
sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    Twitter().run()
    Doge().run()
    print('This job is run every weekday at 5pm.')


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    q = Queue(connection=conn)
    q.enqueue(Twitter().run)
    q.enqueue(Doge().run)
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    Twitter().run()
    Doge().run()
    print('This job is run every weekday at 5pm.')

sched.start()
