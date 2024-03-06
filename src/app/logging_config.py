import logging
from uvicorn.config import LOGGING_CONFIG


def seting_logging_config(debug=False):
    log_formater = "%(asctime)s\t%(levelname)s\t%(message)s"
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_formater)
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s\t%(levelprefix)s %(client_addr)s \t \"%(request_line)s\"\t%(status_code)s"
