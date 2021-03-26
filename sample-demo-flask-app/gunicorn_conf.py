import os
import threading
from codeguru_profiler_agent import Profiler
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] [%(process)d] [%(thread)d %(threadName)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    'loggers': {
        'codeguru_profiler_agent': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    }
})


def post_fork(server, worker):
    """
    post_fork() only runs in workers but not in master.
    """
    server.log.info("Starting profiler for {} in {}".format(os.getpid(), threading.get_ident()))
    worker.profiler = Profiler(profiling_group_name="PythonDemoFlaskApplication")
    worker.profiler.start()
    server.log.info("Profiler started running for worker pid {}: master pid {}.".format(os.getpid(), worker.ppid))
