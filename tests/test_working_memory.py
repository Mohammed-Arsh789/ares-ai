from core.working_memory import WorkingMemory


def test_working_memory_starts_empty():
    memory = WorkingMemory()

    assert memory.is_empty()
    assert len(memory) == 0
    assert memory.fact_count == 0
    assert memory.observation_count == 0
    assert memory.pending_action_count == 0


def test_add_fact():
    memory = WorkingMemory()

    memory.add_fact("Notepad is installed.")

    assert memory.get_facts() == [
        "Notepad is installed."
    ]

    assert memory.fact_count == 1
    assert not memory.is_empty()


def test_fact_memory_is_bounded():
    memory = WorkingMemory(
        max_facts=3
    )

    memory.add_fact("fact 1")
    memory.add_fact("fact 2")
    memory.add_fact("fact 3")
    memory.add_fact("fact 4")

    assert memory.get_facts() == [
        "fact 2",
        "fact 3",
        "fact 4",
    ]

    assert memory.fact_count == 3


def test_get_recent_facts():
    memory = WorkingMemory()

    memory.add_fact("fact 1")
    memory.add_fact("fact 2")
    memory.add_fact("fact 3")

    assert memory.get_facts(
        limit=2
    ) == [
        "fact 2",
        "fact 3",
    ]


def test_add_observation():
    memory = WorkingMemory()

    memory.add_observation(
        "Notepad window appeared."
    )

    assert memory.get_observations() == [
        "Notepad window appeared."
    ]


def test_observation_memory_is_bounded():
    memory = WorkingMemory(
        max_observations=2
    )

    memory.add_observation("one")
    memory.add_observation("two")
    memory.add_observation("three")

    assert memory.get_observations() == [
        "two",
        "three",
    ]


def test_get_recent_observations():
    memory = WorkingMemory()

    memory.add_observation("one")
    memory.add_observation("two")
    memory.add_observation("three")

    assert memory.get_observations(
        limit=1
    ) == [
        "three"
    ]


def test_pending_actions():
    memory = WorkingMemory()

    action_one = {
        "tool": "open_app",
        "arguments": {
            "name": "notepad"
        },
    }

    action_two = {
        "tool": "calculator",
        "arguments": {
            "expression": "2 + 2"
        },
    }

    memory.add_pending_action(
        action_one
    )

    memory.add_pending_action(
        action_two
    )

    assert memory.get_pending_actions() == [
        action_one,
        action_two,
    ]

    assert memory.pending_action_count == 2


def test_remove_pending_action():
    memory = WorkingMemory()

    action = {
        "tool": "open_app"
    }

    memory.add_pending_action(action)

    assert memory.remove_pending_action(
        action
    )

    assert memory.get_pending_actions() == []


def test_remove_missing_pending_action():
    memory = WorkingMemory()

    assert not memory.remove_pending_action(
        "missing"
    )


def test_pending_actions_are_bounded():
    memory = WorkingMemory(
        max_pending_actions=2
    )

    memory.add_pending_action("one")
    memory.add_pending_action("two")
    memory.add_pending_action("three")

    assert memory.get_pending_actions() == [
        "two",
        "three",
    ]


def test_add_convenience_method():
    memory = WorkingMemory()

    memory.add(
        fact="ARES knows this.",
        observation="Tool returned data.",
        pending_action="continue",
    )

    assert memory.get_facts() == [
        "ARES knows this."
    ]

    assert memory.get_observations() == [
        "Tool returned data."
    ]

    assert memory.get_pending_actions() == [
        "continue"
    ]


def test_snapshot():
    memory = WorkingMemory()

    memory.add_fact("fact")
    memory.add_observation("observation")
    memory.add_pending_action("action")

    snapshot = memory.snapshot()

    assert snapshot == {
        "facts": ["fact"],
        "observations": ["observation"],
        "pending_actions": ["action"],
    }


def test_clear_facts():
    memory = WorkingMemory()

    memory.add_fact("one")
    memory.add_fact("two")

    memory.clear_facts()

    assert memory.get_facts() == []
    assert memory.observation_count == 0
    assert memory.pending_action_count == 0


def test_clear_observations():
    memory = WorkingMemory()

    memory.add_observation("one")
    memory.add_observation("two")

    memory.clear_observations()

    assert memory.get_observations() == []


def test_clear_pending_actions():
    memory = WorkingMemory()

    memory.add_pending_action("one")
    memory.add_pending_action("two")

    memory.clear_pending_actions()

    assert memory.get_pending_actions() == []


def test_clear_everything():
    memory = WorkingMemory()

    memory.add_fact("fact")
    memory.add_observation("observation")
    memory.add_pending_action("action")

    memory.clear()

    assert memory.is_empty()
    assert len(memory) == 0


def test_zero_or_negative_limits_are_rejected():
    for kwargs in (
        {"max_facts": 0},
        {"max_facts": -1},
        {"max_observations": 0},
        {"max_observations": -1},
        {"max_pending_actions": 0},
        {"max_pending_actions": -1},
    ):
        try:
            WorkingMemory(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Expected ValueError."
            )


def test_limit_zero_returns_empty_list():
    memory = WorkingMemory()

    memory.add_fact("fact")
    memory.add_observation("observation")
    memory.add_pending_action("action")

    assert memory.get_facts(
        limit=0
    ) == []

    assert memory.get_observations(
        limit=0
    ) == []

    assert memory.get_pending_actions(
        limit=0
    ) == []