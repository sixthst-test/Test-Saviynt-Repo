"""Main entry point"""

import os

from sscil.webapp.gunicorn import GunicornLogger, StandaloneApplication

from hello_api.server import app

WORKERS = int(os.environ.get("GUNICORN_WORKERS", "4"))
PORT = os.environ.get("GUNICORN_PORT", "8000")

if __name__ == "__main__":
    options = {
        "bind": f"0.0.0.0:{PORT}",
        "workers": WORKERS,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": GunicornLogger,
    }

    StandaloneApplication(app, options).run()
