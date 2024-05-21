from datetime import datetime, timedelta

from fastapi import Depends
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from sscil.webapp.fastapi_util import AppBuilder

from hello_api import APP_NAME, START_TIME, VERSION, env
from hello_api.config import api_keys, cors_config, get_api_key, group_role_mapping, oauth_config
from hello_api.v1.routes import router as v1_router


def additional_instrumentation() -> None:
    """Demonstrating how to pass in additional observability instrumentation"""
    RequestsInstrumentor().instrument()


app = (
    AppBuilder(title=APP_NAME, version=VERSION, docs_url="/docs")
    .with_oauth_config(oauth_config)
    .with_group_role_mapping(group_role_mapping[env])
    .with_cors_config(cors_config)
    .with_apikey_config(api_keys.get(env, {}))
    .with_additional_instrumentation(additional_instrumentation)
    .build()
)

app.include_router(
    v1_router,
    prefix="/v1",
    tags=["v1"],
    dependencies=[Depends(get_api_key)],
)


@app.get("/health")
async def health() -> str:
    """Endpoint that the cluster calls to check if we're up."""
    return "ok"


@app.get("/")
@app.get("/status")
def status() -> dict[str, str | timedelta]:
    """
    Returns the status of the application as a dictionary with the following keys:
    - version: The version of the application.
    - uptime: The duration the application has been running.
    """

    return {
        "service": APP_NAME,
        "version": VERSION,
        "uptime": datetime.now() - START_TIME,
    }
