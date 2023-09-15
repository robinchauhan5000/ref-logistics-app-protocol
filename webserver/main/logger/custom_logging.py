import logging
from logging_loki import LokiHandler
import sys

#logger.basicConfig()
root = logging.getLogger()
root.setLevel(logging.INFO)
root.propagate = False

handler = logging.StreamHandler(sys.stdout)
lokiHandler = LokiHandler(
    url="http://3.6.46.226:3100/api/prom/push",
    tags={'app': 'logistics'}
)

#handler.setLevel(logger.INFO)
# formatter = logging.Formatter('%(process)d %(thread)d %(asctime)s [%(name)s][%(levelname)s]::%(message)s')
# formatter = logging.Formatter(json.dumps({'level':'%(levelname)s', 'message': '%(message)s'}))
log_format = '{"level": "%(levelname)s", "message": %(message)s}'
loki_formatter = logging.Formatter(log_format)
handler.setFormatter(loki_formatter)
lokiHandler.setFormatter(loki_formatter)

root.addHandler(handler)
root.addHandler(lokiHandler)


def log(*args,**kwargs):
    logging.info(*args)


def log_error(*args, **kwargs):
    logging.exception(*args)


def debug(*args,**kwargs):
    logging.debug(*args)