from workspace import (
    WorkspaceContext,
    WorkspaceManager,
    WorkspaceSearch,
)


def test_create_workspace(tmp_path):

    from workspace import (
        WorkspaceStorage,
    )

    storage = WorkspaceStorage(
        root=str(tmp_path)
    )

    manager = WorkspaceManager(
        storage=storage
    )

    workspace = manager.create(
        "ARES",
        "ARES development project",
    )

    assert workspace.name == "ARES"

    assert manager.active_id == (
        workspace.workspace_id
    )


def test_workspace_persistence(tmp_path):

    from workspace import (
        WorkspaceStorage,
    )

    storage = WorkspaceStorage(
        root=str(tmp_path)
    )

    manager = WorkspaceManager(
        storage=storage
    )

    workspace = manager.create(
        "Coding",
        "Coding projects",
    )

    loaded = manager.open(
        workspace.workspace_id
    )

    assert loaded.name == "Coding"


def test_workspace_context():

    context = WorkspaceContext()

    context.set(
        "language",
        "Python",
    )

    assert (
        context.get("language")
        == "Python"
    )

    context.remove(
        "language"
    )

    assert (
        context.get("language")
        is None
    )


def test_workspace_search():

    from workspace import Workspace

    workspace = Workspace(
        name="ARES Development",
        description="AI project",
    )

    search = WorkspaceSearch()

    result = search.search(
        workspace,
        "ARES",
    )

    assert len(result) == 1