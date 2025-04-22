import logging
from datetime import datetime
import sys
def get_logger():
    log_date = datetime.today().strftime('%m-%d')

    file_handler = logging.FileHandler("..\\email_process_" + log_date + ".log", mode='a', encoding="utf8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s %(name)s:\t%(message)s'
    ))
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s %(levelname)s] %(message)s',
        datefmt="%Y/%m/%d %H:%M:%S"
    ))
    console_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=min(logging.INFO, logging.DEBUG),
        # handlers=[file_handler, console_handler],
        handlers=[file_handler],
    )

    return logging.getLogger(__name__)
get_logger()