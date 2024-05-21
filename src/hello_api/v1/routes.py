"""v1 routes"""

# pylint: disable=broad-exception-raised, broad-exception-caught

import asyncio

import requests
from fastapi import APIRouter
from loguru import logger
from opentelemetry import metrics, trace
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from sscil.webapp.auth import login_required
from starlette.requests import Request

from hello_api.v1.logic import say_goodbye, say_hi

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

router = APIRouter()


@router.get("/outgoing-http-call")
def call_http() -> str:
    """Example to create spans and demo tracing."""
    with tracer.start_as_current_span("hello-api.outgoing-http-call") as span:
        span.set_attributes({"language": "python-otel-aws", "signal": "trace"})
        span.add_event("Making a request to https://aws.amazon.com")
        logger.info("Making a request to https://aws.amazon.com")
        requests.get("https://aws.amazon.com", timeout=30)
        logger.info("Response received https://aws.amazon.com")

        # As a part of this API, we are returning the traceId that was generated for
        # this call. This is just an example and not required.
        otel_trace_id_decimal = trace.get_current_span().get_span_context().trace_id
        otel_trace_id_hex = f"{otel_trace_id_decimal:032x}"
        return f'{{"traceId": "{otel_trace_id_hex}"}}'


@router.get("/exception")
def throw_exception():  # noqa: ANN201
    """Example to throw an exception"""
    msg = "Test exception"
    raise Exception(msg)  # noqa: TRY002


@router.get("/handled-exception")
def catch_exception() -> None:
    """Example of catching an exception and recording an exception in the span"""
    try:
        msg = "This is a test exception"
        raise Exception(msg)  # noqa: TRY301, TRY002
    except Exception as ex:  # noqa: BLE001
        trace.get_current_span().record_exception(ex)


# pylint: disable=too-few-public-methods
class HiGoodbyeResponse(BaseModel):
    """Hi/Goodbye response."""

    greeting: str


@router.get("/say-hi", response_model=HiGoodbyeResponse)
def hi_world(name: str) -> dict:
    """Example /say-hi route"""
    return say_hi(name)


@router.get("/protected-hi")
@login_required(role="readers")
async def protected_hi(request: Request) -> dict:
    """An example login-protected hi.
    Uses the `sub` (subject) of the access token to say hi to"""
    logger.warning(request)
    if request.headers.get("x-auth-token"):
        return {"greeting": "Hi coreservices-dev@sixthstreet.com!"}
    return say_hi(request.state.access_token["sub"])


# pylint: disable=too-few-public-methods
class GoodbyePayload(BaseModel):
    """Goodbye Route name payload."""

    name: str


@router.post("/protected-goodbye", response_model=HiGoodbyeResponse)
@login_required(role="readers")
# pylint: disable=unused-argument
async def protected_delayed_goodbye(request: Request, name_input: GoodbyePayload) -> dict:  # noqa: ARG001
    """An example login-protected goodbye POST route."""
    logger.info(f"The name_input is {name_input}")
    # Added sleep timer to display loading symbol longer on front-end
    await asyncio.sleep(3)
    return say_goodbye(name_input.name)
