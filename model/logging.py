from pathlib import Path
from datetime import date
import time
import logging


class Logger():
    LOG_PATH = Path("log/log.txt")

    @classmethod
    def write_logfile(cls, message):
        with open(cls.LOG_PATH, "a") as log_file:
            current_time = time.strftime("%H:%M:%S ")
            message = current_time + message
            log_file.write(message)

    @classmethod
    def clear_logs(cls):
        with open(cls.LOG_PATH, 'w') as log_file:
            current_time = time.strftime("%H:%M:%S")
            print(current_time)
            log_header = "VirWalk logfile - {} {} {}".format(date.today(), current_time, "\n\n")
            log_file.write(log_header)
            print(date.today())

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
    def timer(function):
        def wrapper(*args, **kw):
            t_start = time.time()
            result = function(*args, **kw)
            t_end = time.time()
            print(function.__name__, args, kw, t_end - t_start, "fogat")
            return result
        return wrapper

    @staticmethod
    def log_warning():
        logging.basicConfig(filename="logging_messages.log", level=logging.WARNING, format='%(asctime)s: %(levelname)s')
        logging.warning('Mouse out from the window mouse_x={}, mouse_y={}'.format(5, 4))

    @staticmethod
    def log_file_not_found(path):
        logging.basicConfig(filename="logging_messages.log", level=logging.ERROR, format='%(asctime)s: %(levelname)s')
        logging.error('{} file not found!'.format(path))
