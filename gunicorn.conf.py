import os, multiprocessing
from config import Config


bind = f"{Config.APP_HOST}:{Config.APP_PORT}"


workers = 2 * multiprocessing.cpu_count()
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 20
keepalive = 5

loglevel = "error"
accesslog = os.path.join(Config.CURRENT_DIR, "logs", "access.log")
errorlog = os.path.join(Config.CURRENT_DIR, "logs", "error.log")

keyfile = "key.pem" if os.path.exists("key.pem") else None
certfile = "cert.pem" if os.path.exists("cert.pem") else None

def ssl_context(conf, default_ssl_context_factory):
    import ssl

    context = default_ssl_context_factory()
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    return context
