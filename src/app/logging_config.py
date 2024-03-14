import os
import pickle
import struct
from typing import Optional
import logging
from logging.handlers import (
    TimedRotatingFileHandler,
    DatagramHandler
)

from uvicorn.config import LOGGING_CONFIG
from pydantic import AnyUrl
import msgpack


def seting_logging_config(server_name="",logfile_path="./", debug=False, log_server_url: Optional[AnyUrl] = None):
    # 基础配置
    log_formater = f"{server_name}\t"+"%(asctime)s\t%(levelname)s\t%(module)s\t%(message)s"
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_formater)
    root_logger = logging.getLogger()
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = log_formater
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = f"{server_name}\t"+"%(asctime)s\t%(levelname)s\t\
        %(client_addr)s \t%(request_line)s\t%(status_code)s"
    # uvicorn log config
    if not log_server_url:
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
        error_handler = TimedRotatingFileHandler(
            filename=f"{logfile_path}_error.log", when="D", interval=2)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(log_formater))
        root_logger.addHandler(error_handler)
    elif log_server_url.scheme == "udp":

        LOGGING_CONFIG["handlers"]["access_udp"] = {
            "class": "logging.handlers.DatagramHandler",
            "formatter": "access",
            "level": "INFO",
            "host": log_server_url.host,
            "port": log_server_url.port
        }
        LOGGING_CONFIG["loggers"]["uvicorn.access"]["handlers"].append(
            "access_udp")
        udp_handler = DatagramHandler(
            host=log_server_url.host,
            port=log_server_url.port
        )
        udp_handler.setLevel(logging.ERROR)
        udp_handler.setFormatter(logging.Formatter(log_formater))
        root_logger.addHandler(udp_handler)


def make_udp_msgpack(self, record):
    d = self.format(record)
    bd = msgpack.packb({"msg": d})
    return bd

DatagramHandler.makePickle = make_udp_msgpack
