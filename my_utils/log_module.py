import logging
import os
from logging import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def config_log(log_name, log_level):
    log_name = log_name
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': log_level,
                'formatter': 'standard',
                'backupCount': 7,
                'interval': 1,
                'when': 'midnight',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': BASE_DIR + "/logs/" + log_name + ".log"
            },
        },
        'loggers': {
            log_name: {
                # 'handlers': ['console', 'file'],
                'handlers': ['console'],
                'level': log_level,
            },
        }
    }

    logging.config.dictConfig(LOGGING)

if(str(os.getenv('ENV_SCRIPT')) == 'prod'):
    log_level = 'INFO'
else:
    log_level = 'DEBUG'


config_log('socialapi', log_level)
logger_socialapi = logging.getLogger('socialapi')