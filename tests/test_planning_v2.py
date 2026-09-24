from core.planner import Planner
from core.task import Plan, Task, TaskStatus
from core.task_graph import (
    DependencyCycleError,
    TaskGraph,
)
from core.orchestrator import Orchestrator


def test_planner_creates_calculator_task():
    planner = Planner()

    plan = planner.create_plan("calculate 25 * 8")

    assert isinstance(plan, Plan)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].tool == "calculator"
    assert plan.tasks[0].arguments["expression"] == "25 * 8"


def test_planner_creates_weather_task():
    planner = Planner()

    plan = planner.create_plan("weather in Bengaluru")

    assert len(plan.tasks) == 1
    assert plan.tasks[0].tool == "weather"
    assert plan.tasks[0].arguments["location"] == "Bengaluru"


def test_task_graph_dependencies():
    first = Task(
        name="first",
        tool="test_first",
    )

    second = Task(
        name="second",
        tool="test_second",
        dependencies=[first.task_id],
    )

    plan = Plan(goal="dependency test")
    plan.add_task(first)
    plan.add_task(second)

    graph = TaskGraph(plan)

    ready = graph.ready_tasks()

    assert len(ready) == 1
    assert ready[0].task_id == first.task_id

    first.mark_success("done")

    ready = graph.ready_tasks()

    assert len(ready) == 1
    assert ready[0].task_id == second.task_id


def test_task_graph_detects_cycle():
    first = Task(name="first")
    second = Task(
        name="second",
        dependencies=[first.task_id],
    )

    first.dependencies.append(second.task_id)

    plan = Plan(goal="cycle")
    plan.add_task(first)
    plan.add_task(second)

    try:
        TaskGraph(plan)
        assert False, "Expected DependencyCycleError"
    except DependencyCycleError:
        pass


def test_task_serialization():
    task = Task(
        name="test",
        tool="calculator",
        arguments={"expression": "2 + 2"},
    )

    restored = Task.from_dict(task.to_dict())

    assert restored.name == "test"
    assert restored.tool == "calculator"
    assert restored.arguments["expression"] == "2 + 2"


def test_orchestrator_dry_run():
    planner = Planner()

    plan = planner.create_plan("calculate 10 + 5")

    orchestrator = Orchestrator()

    result = orchestrator.execute_plan(
        plan,
        dry_run=True,
    )

    assert result.success is True
    assert result.output["plan_id"] == plan.plan_id
    assert result.output["summary"]["success"] == 1


def test_orchestrator_executes_registry_tool():
    class FakeRegistry:
        def execute_result(self, name, **kwargs):
            return {
                "success": True,
                "output": f"{name}: {kwargs}",
            }

    planner = Planner()
    plan = planner.create_plan("calculate 10 + 5")

    orchestrator = Orchestrator(
        registry=FakeRegistry(),
    )

    result = orchestrator.execute_plan(plan)

    assert result.success is True
    assert plan.tasks[0].status == TaskStatus.SUCCESS