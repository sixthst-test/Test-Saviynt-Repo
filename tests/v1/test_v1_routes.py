"""
Module containing unit tests for the v1 routes of the Hi Api.

Functions:
- test_say_hi(): Test case for the /say-hi route.
- _mock_login(request, _): Helper function to mock the login process.
- test_protected_hi(mock_login): Test case for the protected /hi route with successful login.
- test_protected_hi_fail_login(): Test case for the protected /hi route with failed login.
"""
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from hello_api.v1.routes import router

app = FastAPI()
app.include_router(router)


client = TestClient(app)


def test_say_hi():
    """
    Test case for the /say-hi route.
    """
    response = client.get("/say-hi", params={"name": "Test"})
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hi Test!"}


def _mock_login(request, _):
    """
    Helper function to mock the login process.
    """
    request.state.access_token = {"sub": "Mock User"}


@patch("sscil.webapp.auth._login_required_impl")
def test_protected_hi(mock_login):
    """
    Test case for the protected /hi route with successful login.
    """
    mock_login.side_effect = _mock_login
    response = client.get("/protected-hi")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hi Mock User!"}


def test_protected_hi_fail_login():
    """
    Test case for the protected /hi route with failed login.
    """
    response = client.get("/protected-hi")
    assert response.status_code == 401
