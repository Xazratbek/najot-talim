import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bind = "unix:/tmp/quranapi-run/gunicorn.sock"
workers = 3
worker_class = "sync"
timeout = 60

accesslog = f"{BASE_DIR}/deploy/local/logs/gunicorn-access.log"
errorlog = f"{BASE_DIR}/deploy/local/logs/gunicorn-error.log"
loglevel = "info"
capture_output = True
pidfile = "/tmp/quranapi-run/gunicorn.pid"
