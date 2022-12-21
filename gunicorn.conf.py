import multiprocessing
from config import Config
import os


bind = f"{Config.APP_HOST}:{Config.APP_PORT}"


workers = multiprocessing.cpu_count() * 2 - 1
threads = 2
worker_class = "gthread"
worker_connections = 1000

timeout = 10
keepalive = 5

loglevel = "error"
accesslog = os.path.join(Config.CURRENT_DIR, "logs", "access.log")
errorlog = os.path.join(Config.CURRENT_DIR, "logs", "error.log")
