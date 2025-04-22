# import email_processor
# from utils_module import log_factory
# import threading
#
# logger = log_factory.get_logger()
# lock = threading.Lock()
#
# def repeat_function():
#     lock.acquire_lock()
#     try:
#         logger.info("scheduler start get and process mail from inbox...")
#         email_processor.process_email()
#     finally:
#         lock.release_lock()
#
# # 创建一个每隔5秒重复执行的定时器
# timer = threading.Timer(90, repeat_function)
#
#
# # 启动定时器
# timer.start()