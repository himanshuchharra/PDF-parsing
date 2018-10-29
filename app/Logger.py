from logging.handlers import TimedRotatingFileHandler
import logging
from constants import LOG_PATH
import os

# Create log path folder if it does not exist
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

# Log file name
logFileName = LOG_PATH + "StatementLog.log"

# initialize logger
logger = logging.getLogger(logFileName)
# create logger policy
handler = TimedRotatingFileHandler(logFileName, when='midnight', interval=1, backupCount=30, encoding=None,
                                   delay=False, utc=False)
# set log formatting
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
handler.close()


# 'application' code
def debug(s):
    logger.debug(s)


def info(s):
    logger.info(s)


def warning(s):
    logger.warning(s)


def error(s):
    logger.error(s)


def critical(s):
    logger.critical(s)
