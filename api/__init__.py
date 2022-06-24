from flask import Flask
import logging

app = Flask(__name__)


def log_creator(name, file_name, level=logging.DEBUG):
    local_logger = logging.getLogger(name)
    local_logger.setLevel(level)

    fh = logging.FileHandler(f"../{file_name}.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    local_logger.addHandler(fh)
    return local_logger


logger = log_creator("code_info", "code_log")

from api import router
