from security.action import ActionRequest
from security.decision import DecisionType
from security.gateway import SecurityGateway
from security.permissions import PermissionLevel


def test_unpermitted_read_is_denied():

    gateway = SecurityGateway()

    request = ActionRequest(
        tool="files",
        action="read",
        arguments={
            "path": "example.txt"
        },
    )

    decision = gateway.evaluate(
        request
    )

    assert decision.decision == (
        DecisionType.DENY
    )


def test_permitted_read_is_allowed():

    gateway = SecurityGateway()

    gateway.permissions.grant(
        "files",
        PermissionLevel.READ,
    )

    request = ActionRequest(
        tool="files",
        action="read",
    )

    decision = gateway.evaluate(
        request
    )

    assert decision.decision == (
        DecisionType.ALLOW
    )


def test_delete_requires_confirmation():

    gateway = SecurityGateway()

    gateway.permissions.grant(
        "files",
        PermissionLevel.ADMIN,
    )

    request = ActionRequest(
        tool="files",
        action="delete",
    )

    decision = gateway.evaluate(
        request
    )

    assert decision.decision == (
        DecisionType.CONFIRM
    )