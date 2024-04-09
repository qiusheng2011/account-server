
import logging
import logging.handlers
import msgpack

import pydantic


def setting_logging_config(
        worker_name="",
        logfile_path="",
        debug=False,
        log_server_url: pydantic.AnyUrl | None = None
):
    log_formater = (f"{worker_name}\t"
                    "%(asctime)s\t"
                    "%(levelname)s\t"
                    "%(module)s\t"
                    "%(message)s"
                    )
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_formater)

    root_logger = logging.getLogger()
    if not log_server_url and logfile_path:
        work_info_log_hander = logging.handlers.TimedRotatingFileHandler(
            filename=f"{logfile_path}_info.log",
            when="D",
            interval=2,
        )
        work_info_log_hander.setLevel(log_level)
        root_logger.addHandler(work_info_log_hander)

        woker_error_log_handler = logging.handlers.TimedRotatingFileHandler(
            filename=f"{logfile_path}_error.log",
            when="W"
        )
        woker_error_log_handler.setLevel(logging.ERROR)
        root_logger.addHandler(woker_error_log_handler)

    if log_server_url:
        if log_server_url.scheme == "udp":
            udp_hander = logging.handlers.DatagramHandler(
                host=log_server_url.host,
                port=log_server_url.port
            )
            fmt_str = (
                    f"{worker_name}\t"
                    "%(asctime)s\t"
                    "%(levelname)s\t"
                    "%(message)s"
                )
            udp_hander.setFormatter(logging.Formatter(fmt=fmt_str))
            udp_hander.setLevel(logging.INFO)
            root_logger.addHandler(udp_hander)

            def make_udp_msgpack(self, record):
                d = self.format(record)
                bd = msgpack.packb({"msg": d})
                return bd if bd else b""
            logging.handlers.DatagramHandler.makePickle = make_udp_msgpack
