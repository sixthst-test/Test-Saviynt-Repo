"Top level module for FastAPI service"

import os
from datetime import datetime
from importlib.metadata import metadata

from sscil import loghelper

PACKAGE_METADATA = metadata(__name__)
APP_NAME = "hello-api"  # This is the actual service.name that is used for Otel resource and Status API
VERSION = PACKAGE_METADATA["Version"]
COMMIT_SHA = "replaced_programmatically_when_published"
START_TIME = datetime.now()

env = os.getenv("SSTP_ENVIRONMENT", "local")
loghelper.configure(APP_NAME, extra={"version": VERSION, "commit_sha": COMMIT_SHA})
