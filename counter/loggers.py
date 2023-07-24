import logging
from logging.handlers import RotatingFileHandler
import datetime

logging.basicConfig(
        handlers=[RotatingFileHandler('log/{:%Y-%m-%d}.log'.format(datetime.datetime.now()), maxBytes=100000, backupCount=10)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
