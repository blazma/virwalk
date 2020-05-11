from pathlib import Path
from datetime import date
import time
import logging


class Logger:
    RUNTIME_LOG_PATH = Path("logs/runtime.txt")
    LOGGING_MESSAGES_PATH = Path("logs/logging_messages.log")
    DEBUGGER = None

    @classmethod
    def write_logfile(cls, message):
        if cls.DEBUGGER == 1:
            with open(cls.RUNTIME_LOG_PATH, "a") as log_file:
                current_time = time.strftime("%H:%M:%S ")
                message = current_time + message
                log_file.write(message)

    @classmethod
    def clear_logs(cls):
        logging.basicConfig(filename=Logger.LOGGING_MESSAGES_PATH, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

        with open(Logger.LOGGING_MESSAGES_PATH, 'w'):
            log_header = "VirWalk logfile\nProgram started\n\n"
            logging.info(log_header)
            logging.info('logging_messages.logs has been cleared')

        with open(Logger.RUNTIME_LOG_PATH, 'w') as log_file:
            current_time = time.strftime("%H:%M:%S")
            runtime_log_header = "VirWalk runtime file - {} {} {}".format(date.today(), current_time,
                                                                  "\nProgram started\n\n")
            log_file.write(runtime_log_header)
            logging.info('logs.txt has been cleared')

    @staticmethod
    def runtime(function):
        def wrapper(*args, **kw):
            t_start = time.time()
            result = function(*args, **kw)
            t_end = time.time()
            message = "{} {} {} {} {}".format(function.__name__, args, kw, t_end - t_start, "\n")
            Logger.write_logfile(message)

            return result
        return wrapper

    @staticmethod
    def log_warning(message):
        logging.basicConfig(filename=Logger.LOGGING_MESSAGES_PATH, level=logging.WARNING, format='%(asctime)s: %(levelname)s: %(message)s')
        logging.warning(message)

    @staticmethod
    def log_error(message):
        logging.basicConfig(filename=Logger.LOGGING_MESSAGES_PATH, level=logging.ERROR, format='%(asctime)s: %(levelname)s: %(message)s')
        logging.error(message)

    @staticmethod
    def log_info(message):
        logging.basicConfig(filename=Logger.LOGGING_MESSAGES_PATH, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')
        logging.info(message)
