"""
ARES Test Tool
Step 175
"""

from .base import Tool


class EchoTool(Tool):

    name = "echo"

    description = (
        "Returns text for testing the ARES tool system."
    )

    dangerous = False

    def execute(
        self,
        text: str = "",
    ):

        return {
            "success": True,
            "text": text,
        }