from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from process_module import email_processor
from utils_module import log_factory

logger = log_factory.get_logger()
if __name__ == '__main__':
    schedule = BlockingScheduler(executors={'default': ThreadPoolExecutor(1)})
    schedule.add_job(email_processor.process_email, "cron", second='*/50')

    logger.info(schedule.print_jobs())
    schedule.start()

