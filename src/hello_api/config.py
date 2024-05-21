"""Configuration for the app"""
import os

from fastapi import Security
from fastapi.security import APIKeyHeader
from sscil.webapp.auth import OAuthConfig
from sscil.webapp.config import CorsConfig

OAUTH_TENANT = os.getenv("OAUTH_TENANT", "sixthstreet.okta.com")
AUTH_SERVER = os.getenv("AUTH_SERVER", "default")
AUDIENCE = os.getenv("AUDIENCE", "api://default")
CLIENT_ID = os.getenv("CLIENT_ID", "0oafyc9okr12ku0Wo5d7")

oauth_config = OAuthConfig(
    OAUTH_TENANT,
    AUTH_SERVER,
    AUDIENCE,
    CLIENT_ID,
)

# The `group_role_mapping` maps Okta groups to logical roles.  We use the logical roles to protect the routes
#
# We have 2 logical roles:
#   1. readers: this is required for full access read role for the Hello API Service members
#   2. writers: this is required for full access write role for the Hello API Service members
#
group_role_mapping = {
    # fmt: off
    "dev": {
        "All-Sixth Street Staff": "readers",
    },
    "test": {
        "Hello API Users [Test]": "readers",
        "Hello API Writers [Test]": "writers",
    },
    "prod": {
        "Hello API Users [Prod]": "readers",
        "Hello API Writers [Prod]": "writers",
    },
    # fmt: on
}
group_role_mapping["local"] = group_role_mapping["dev"]

api_keys = {
    "local": {
        # local dev key = hello123
        "27cc6994fc1c01ce6659c6bddca9b69c4c6a9418065e612c69d110b3f7b11f8a": {
            "caller": "LocalDev",
            "expiration": "2099-01-01",
            "roles": {"readers", "writers"},
        },
    },
    "dev": {
        # local dev key = hello123
        "27cc6994fc1c01ce6659c6bddca9b69c4c6a9418065e612c69d110b3f7b11f8a": {
            "caller": "LocalDev",
            "expiration": "2099-01-01",
            "roles": {"readers", "writers"},
        },
    },
}

cors_config = CorsConfig(
    allow_origins=["http://localhost:3000", "https://hello.dev.aws.sstp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: Change this back and forth to switch between using
#    'X-Auth-Token' (API Key) and 'Authorization' (Bearer Tokens)
#    Bearer tokens can be obtained by viewing an API request's header params in the UI with Chrome Dev Tools 
def get_docs_auth_method() -> str:
    """Get the authorization token header to use"""
    return os.getenv("DOCS_AUTH", "X-Auth-Token")


docs_auth_method = get_docs_auth_method()
_api_key_header = APIKeyHeader(name=docs_auth_method, scheme_name="X-Auth-Token", auto_error=False)


def get_api_key(api_key_header: str = Security(_api_key_header)) -> str:
    """Get the API key"""
    return api_key_header
