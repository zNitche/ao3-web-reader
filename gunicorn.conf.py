import os, ssl, multiprocessing
from config import Config


bind = f"{Config.APP_HOST}:{Config.APP_PORT}"


workers = 2 * multiprocessing.cpu_count() + 1
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 20
keepalive = 5

loglevel = "error"
accesslog = os.path.join(Config.CURRENT_DIR, "logs", "access.log")
errorlog = os.path.join(Config.CURRENT_DIR, "logs", "error.log")

keyfile = "key.pem" if os.path.exists("key.pem") else None
certfile = "cert.pem" if os.path.exists("cert.pem") else None

__is_ssl_enabled = True if keyfile is not None and certfile is not None else False

ssl_version = ssl.PROTOCOL_TLS if __is_ssl_enabled else None
cert_reqs = True if __is_ssl_enabled else False
