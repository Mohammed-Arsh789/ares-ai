"""
ARES Workspace Search
"""

from __future__ import annotations


class WorkspaceSearch:

    def search(
        self,
        workspace,
        query: str,
    ) -> list[dict]:

        query = query.strip().lower()

        if not query:
            return []

        results = []

        if query in workspace.name.lower():

            results.append({
                "type": "workspace",
                "field": "name",
                "value": workspace.name,
            })

        if query in workspace.description.lower():

            results.append({
                "type": "workspace",
                "field": "description",
                "value": workspace.description,
            })

        return results