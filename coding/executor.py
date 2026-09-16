from pathlib import Path

from .models import ChangeProposal, ChangeType
from .validator import CodeValidator


class CodingExecutor:
    """
    Handles proposed changes.

    Default behavior is dry-run.
    Actual writes require explicit approval.
    """

    def __init__(
        self,
        validator: CodeValidator | None = None,
    ):
        self.validator = validator or CodeValidator()

    def validate_proposal(
        self,
        proposal: ChangeProposal,
    ) -> dict:
        if proposal.change_type == ChangeType.DELETE:
            return {
                "valid": True,
                "action": "delete",
                "path": proposal.path,
            }

        if proposal.proposed_content is None:
            return {
                "valid": False,
                "action": proposal.change_type.value,
                "path": proposal.path,
                "error": "No proposed content supplied.",
            }

        path = Path(proposal.path)

        if path.suffix.lower() == ".py":
            return self.validator.validate_python_syntax(
                proposal.proposed_content,
                filename=str(path),
            )

        return {
            "valid": True,
            "action": proposal.change_type.value,
            "path": proposal.path,
            "error": None,
        }

    def apply_proposal(
        self,
        proposal: ChangeProposal,
        approved: bool = False,
    ) -> dict:
        if not approved:
            return {
                "success": False,
                "applied": False,
                "path": proposal.path,
                "error": "Proposal was not approved.",
            }

        validation = self.validate_proposal(proposal)

        if not validation.get("valid", False):
            return {
                "success": False,
                "applied": False,
                "path": proposal.path,
                "error": validation.get("error"),
            }

        path = Path(proposal.path)

        if proposal.change_type == ChangeType.CREATE:
            if path.exists():
                return {
                    "success": False,
                    "applied": False,
                    "path": str(path),
                    "error": "File already exists.",
                }

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                proposal.proposed_content or "",
                encoding="utf-8",
            )

        elif proposal.change_type == ChangeType.MODIFY:
            if not path.exists():
                return {
                    "success": False,
                    "applied": False,
                    "path": str(path),
                    "error": "Target file does not exist.",
                }

            path.write_text(
                proposal.proposed_content or "",
                encoding="utf-8",
            )

        elif proposal.change_type == ChangeType.DELETE:
            if path.exists():
                path.unlink()

        return {
            "success": True,
            "applied": True,
            "path": str(path),
            "action": proposal.change_type.value,
        }