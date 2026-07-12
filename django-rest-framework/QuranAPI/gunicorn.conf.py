import multiprocessing
import os

bind = os.environ.get("GUNICORN_BIND", "unix:/run/quranapi/gunicorn.sock")
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
timeout = 60
graceful_timeout = 30
keepalive = 5

accesslog = "/var/log/quranapi/gunicorn-access.log"
errorlog = "/var/log/quranapi/gunicorn-error.log"
loglevel = "info"

capture_output = True
pidfile = "/run/quranapi/gunicorn.pid"
