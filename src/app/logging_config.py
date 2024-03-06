import os
import logging
from logging.handlers import (
    TimedRotatingFileHandler
)
from uvicorn.config import LOGGING_CONFIG


def seting_logging_config(logfile_path="./", debug=False):
    # 基础配置
    log_formater = "%(asctime)s\t%(levelname)s\t%(module)s\t%(message)s"
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_formater)

    # uvicorn log config
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = log_formater
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"] = "%(asctime)s\t%(levelname)s\t%(client_addr)s \t%(request_line)s\t%(status_code)s"
    LOGGING_CONFIG["handlers"]["access_file"] = {
        "class": 'logging.handlers.TimedRotatingFileHandler',
        "formatter": "access",
        "level": "INFO",
        "filename": f"{logfile_path}_access.log",
        "when": "D",
        "interval": 2
    }
    LOGGING_CONFIG["loggers"]["uvicorn.access"]["handlers"].append(
        "access_file")

    error_handler = TimedRotatingFileHandler(filename=f"{logfile_path}_error.log", when="D", interval=2)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_formater))
    root_logger = logging.getLogger()
    root_logger.addHandler(error_handler)
