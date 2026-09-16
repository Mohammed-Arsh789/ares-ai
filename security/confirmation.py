"""
ARES Confirmation Manager

Handles actions that require explicit user approval.

The manager does not automatically approve anything.
"""

from __future__ import annotations

import uuid

from .action import ActionRequest


class ConfirmationManager:

    def __init__(self):

        self._pending: dict[
            str,
            ActionRequest,
        ] = {}

    def request(
        self,
        action: ActionRequest,
    ) -> str:

        confirmation_id = str(
            uuid.uuid4()
        )

        self._pending[
            confirmation_id
        ] = action

        return confirmation_id

    def get(
        self,
        confirmation_id: str,
    ):

        return self._pending.get(
            confirmation_id
        )

    def approve(
        self,
        confirmation_id: str,
    ):

        return self._pending.pop(
            confirmation_id,
            None,
        )

    def reject(
        self,
        confirmation_id: str,
    ):

        self._pending.pop(
            confirmation_id,
            None,
        )

    def pending(self):

        return {
            key: value.to_dict()
            for key, value
            in self._pending.items()
        }