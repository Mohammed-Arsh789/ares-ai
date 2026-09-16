"""
ARES Web Capability Description

Used by the planner/router to understand
what the web subsystem can do.
"""

from __future__ import annotations


WEB_CAPABILITIES = {
    "search": {
        "description":
            "Search public web information.",
        "requires_confirmation":
            False,
    },

    "fetch_url": {
        "description":
            "Retrieve a public HTTP/HTTPS page.",
        "requires_confirmation":
            False,
    },

    "current_information": {
        "description":
            "Find recent/current information.",
        "requires_confirmation":
            False,
    },
}


def get_web_capabilities():

    return WEB_CAPABILITIES.copy()