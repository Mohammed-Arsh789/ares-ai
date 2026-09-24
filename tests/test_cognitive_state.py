from core.cognitive_state import CognitiveState


def test_cognitive_state_creates_valid_ids():
    state = CognitiveState()

    assert state.task_id
    assert state.session_id
    assert state.task_id != state.session_id


def test_cognitive_state_initial_values():
    state = CognitiveState()

    assert state.current_goal == ""
    assert state.current_step == 0
    assert state.active_plan is None
    assert state.pending_actions == []
    assert state.observations == []
    assert state.constraints == []
    assert state.facts == []
    assert state.last_decision is None
    assert state.last_tool_result is None
    assert state.failure_count == 0
    assert state.recovery_count == 0
    assert state.status == "idle"


def test_set_goal():
    state = CognitiveState()

    state.set_goal("  Open Notepad  ")

    assert state.current_goal == "Open Notepad"


def test_set_step():
    state = CognitiveState()

    state.set_step(3)

    assert state.current_step == 3


def test_advance_step():
    state = CognitiveState()

    assert state.advance_step() == 1
    assert state.advance_step() == 2
    assert state.current_step == 2


def test_set_plan():
    state = CognitiveState()

    plan = {
        "steps": [
            "open application",
            "perform action",
        ]
    }

    state.set_plan(plan)

    assert state.active_plan == plan


def test_pending_actions():
    state = CognitiveState()

    action_one = {
        "tool": "open_app",
        "arguments": {"name": "notepad"},
    }

    action_two = {
        "tool": "calculator",
        "arguments": {"expression": "2 + 2"},
    }

    state.add_pending_action(action_one)
    state.add_pending_action(action_two)

    assert len(state.pending_actions) == 2

    assert state.remove_pending_action(
        action_one
    )

    assert action_one not in state.pending_actions
    assert action_two in state.pending_actions


def test_remove_missing_pending_action():
    state = CognitiveState()

    assert not state.remove_pending_action(
        "does-not-exist"
    )


def test_clear_pending_actions():
    state = CognitiveState()

    state.add_pending_action("one")
    state.add_pending_action("two")

    state.clear_pending_actions()

    assert state.pending_actions == []


def test_observations_constraints_and_facts():
    state = CognitiveState()

    state.add_observation("Notepad opened.")
    state.add_constraint("Do not modify files.")
    state.add_fact("The requested application is Notepad.")

    assert state.observations == [
        "Notepad opened."
    ]

    assert state.constraints == [
        "Do not modify files."
    ]

    assert state.facts == [
        "The requested application is Notepad."
    ]


def test_decision_and_tool_result():
    state = CognitiveState()

    decision = {
        "type": "tool",
        "tool": "calculator",
    }

    result = {
        "success": True,
        "value": 4,
    }

    state.set_decision(decision)
    state.set_tool_result(result)

    assert state.last_decision == decision
    assert state.last_tool_result == result


def test_failure_and_recovery_tracking():
    state = CognitiveState()

    assert state.record_failure() == 1
    assert state.record_failure() == 2

    assert state.record_recovery() == 1
    assert state.record_recovery() == 2

    assert state.failure_count == 2
    assert state.recovery_count == 2


def test_status_normalization():
    state = CognitiveState()

    state.set_status("  THINKING  ")

    assert state.status == "thinking"


def test_snapshot():
    state = CognitiveState()

    state.set_goal("Open Notepad")
    state.set_step(2)
    state.add_fact("Notepad is available.")
    state.add_observation("Launcher succeeded.")
    state.set_status("executing")

    snapshot = state.snapshot()

    assert snapshot["task_id"] == state.task_id
    assert snapshot["session_id"] == state.session_id
    assert snapshot["current_goal"] == "Open Notepad"
    assert snapshot["current_step"] == 2
    assert snapshot["facts"] == [
        "Notepad is available."
    ]
    assert snapshot["observations"] == [
        "Launcher succeeded."
    ]
    assert snapshot["status"] == "executing"


def test_reset_task_preserves_session_by_default():
    state = CognitiveState()

    original_session = state.session_id
    original_task = state.task_id

    state.set_goal("Open Notepad")
    state.set_step(4)
    state.add_fact("test")
    state.record_failure()
    state.record_recovery()
    state.set_status("failed")

    state.reset_task()

    assert state.session_id == original_session
    assert state.task_id != original_task

    assert state.current_goal == ""
    assert state.current_step == 0
    assert state.facts == []
    assert state.failure_count == 0
    assert state.recovery_count == 0
    assert state.status == "idle"


def test_clear_creates_fresh_session():
    state = CognitiveState()

    original_session = state.session_id

    state.set_goal("Temporary task")
    state.clear()

    assert state.session_id != original_session
    assert state.current_goal == ""
    assert state.status == "idle"