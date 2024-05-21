"""
This module contains the business logic functions for the Hello Api Example.

Module Functions:
- say_hi(name: str) -> dict: A function that takes a name as input and returns a dictionary with a greeting message.
- say_goodbye(name: str) -> dict: A function that says goodbye to a person.
"""

from loguru import logger
from opentelemetry import trace

tracer = trace.get_tracer_provider().get_tracer(__name__)


@tracer.start_as_current_span("Custom Span Name")
def say_hi(name: str) -> dict:
    """
    A function that takes a name as input and returns a dictionary with a greeting message.

    Args:
        name (str): The name of the person to say hi to.
    """

    logger.info("Saying hi to {}", name)
    return {"greeting": f"Hi {name}!"}


def say_goodbye(name: str) -> dict:
    """
    A function that says goodbye to a person.

    Args:
        name (str): The name of the person to say goodbye to.
    """

    logger.info("Saying goodbye to {}", name)
    return {"greeting": f"Goodbye {name}!"}
