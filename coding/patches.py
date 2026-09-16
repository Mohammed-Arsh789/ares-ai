from dataclasses import dataclass

from .models import ChangeProposal, ChangeType


@dataclass
class Patch:
    """
    Represents a proposed text replacement.
    """

    path: str
    old_text: str
    new_text: str
    reason: str = ""

    def to_change_proposal(self) -> ChangeProposal:
        return ChangeProposal(
            path=self.path,
            change_type=ChangeType.MODIFY,
            original_content=self.old_text,
            proposed_content=self.new_text,
            reason=self.reason,
        )


class PatchBuilder:
    """
    Creates change proposals without writing files.
    """

    def create_file(
        self,
        path: str,
        content: str,
        reason: str = "",
    ) -> ChangeProposal:
        return ChangeProposal(
            path=path,
            change_type=ChangeType.CREATE,
            proposed_content=content,
            reason=reason,
        )

    def modify_file(
        self,
        path: str,
        original_content: str,
        proposed_content: str,
        reason: str = "",
    ) -> ChangeProposal:
        return ChangeProposal(
            path=path,
            change_type=ChangeType.MODIFY,
            original_content=original_content,
            proposed_content=proposed_content,
            reason=reason,
        )

    def delete_file(
        self,
        path: str,
        original_content: str | None = None,
        reason: str = "",
    ) -> ChangeProposal:
        return ChangeProposal(
            path=path,
            change_type=ChangeType.DELETE,
            original_content=original_content,
            reason=reason,
        )