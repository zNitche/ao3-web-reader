import multiprocessing
from config import Config
import os


bind = f"{Config.APP_HOST}:{Config.APP_PORT}"


workers = 2 * multiprocessing.cpu_count() + 1
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 20
keepalive = 5

loglevel = "error"
accesslog = os.path.join(Config.CURRENT_DIR, "logs", "access.log")
errorlog = os.path.join(Config.CURRENT_DIR, "logs", "error.log")
