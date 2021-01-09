from apscheduler.schedulers.blocking import BlockingScheduler
from stock_automation import robinhood

sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(robinhood, 'interval', hours=8, start_date='2020-12-26 08:00:00',
              end_date='2021-12-31 11:59:59')

sched.start()

