from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from core.cognitive_state import CognitiveState
from core.working_memory import WorkingMemory


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BrainResult:
    """
    Result returned by the ARES brain after processing a request.
    """

    success: bool

    response: str = ""

    executed: bool = False

    decision: Any = None

    execution_result: Any = None

    verification: Any = None

    reflection: Any = None

    error: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


class ARESBrain:
    """
    Central orchestration layer for ARES cognition.

    The Brain coordinates:

    - context
    - cognitive reasoning
    - decisions
    - planning
    - tool execution
    - verification
    - reflection
    - cognitive state
    - working memory
    - long-term memory

    The Brain itself does not perform tool-specific work.
    """

    def __init__(
        self,
        *,
        cognitive_core: Any = None,
        context_manager: Any = None,
        planner: Any = None,
        orchestrator: Any = None,
        verification_engine: Any = None,
        reflection_engine: Any = None,
        memory_bridge: Any = None,
        cognitive_state: CognitiveState | None = None,
        working_memory: WorkingMemory | None = None,
    ) -> None:
        self.cognitive_core = cognitive_core

        self.context_manager = (
            context_manager
        )

        self.planner = planner

        self.orchestrator = orchestrator

        self.verification_engine = (
            verification_engine
        )

        self.reflection_engine = (
            reflection_engine
        )

        self.memory_bridge = (
            memory_bridge
        )

        self.cognitive_state = (
            cognitive_state
            if cognitive_state is not None
            else CognitiveState()
        )

        self.working_memory = (
            working_memory
            if working_memory is not None
            else WorkingMemory()
        )

    # ------------------------------------------------------------------
    # Main processing
    # ------------------------------------------------------------------

    def process(
        self,
        user_input: str,
        *,
        session_context: Any = None,
    ) -> BrainResult:
        """
        Process a user request through the ARES cognitive pipeline.
        """

        if not isinstance(user_input, str):
            raise TypeError(
                "user_input must be a string."
            )

        user_input = user_input.strip()

        if not user_input:
            raise ValueError(
                "Cannot process empty input."
            )

        logger.info(
            "ARES processing request."
        )

        self._begin_task(
            user_input=user_input,
            session_context=session_context,
        )

        context = self._build_context(
            user_input=user_input,
            session_context=session_context,
        )

        self._record_context(
            context
        )

        decision = self._make_decision(
            user_input=user_input,
            context=context,
        )

        self.cognitive_state.set_decision(
            decision
        )

        self._record_working_memory(
            fact={
                "type": "decision",
                "value": decision,
            }
        )

        decision_type = self._decision_type(
            decision
        )

        if decision_type == "conversation":
            result = self._handle_conversation(
                decision
            )

        elif decision_type == "clarification":
            result = self._handle_clarification(
                decision
            )

        elif decision_type == "refuse":
            result = self._handle_refusal(
                decision
            )

        elif decision_type == "plan":
            result = self._handle_plan(
                decision=decision,
                user_input=user_input,
                context=context,
            )

        elif decision_type == "tool":
            result = self._handle_tool(
                decision=decision,
                user_input=user_input,
                context=context,
            )

        else:
            result = BrainResult(
                success=False,
                response=(
                    "ARES could not determine "
                    "how to handle the request."
                ),
                decision=decision,
                error=(
                    f"Unsupported decision type: "
                    f"{decision_type}"
                ),
            )

        self._finalize_task(
            result=result
        )

        return result

    # ------------------------------------------------------------------
    # Task lifecycle
    # ------------------------------------------------------------------

    def _begin_task(
        self,
        *,
        user_input: str,
        session_context: Any,
    ) -> None:
        """
        Initialize state for a new request.
        """

        self.cognitive_state.reset_task(
            keep_session=True
        )

        self.cognitive_state.set_goal(
            user_input
        )

        self.cognitive_state.set_status(
            "thinking"
        )

        self.working_memory.clear()

        self.working_memory.add_fact(
            {
                "type": "user_input",
                "value": user_input,
            }
        )

        if session_context is not None:
            self.working_memory.add_fact(
                {
                    "type": "session_context",
                    "value": session_context,
                }
            )

    def _finalize_task(
        self,
        *,
        result: BrainResult,
    ) -> None:
        """
        Update final cognitive state after processing.
        """

        if result.success:
            if result.executed:
                self.cognitive_state.set_status(
                    "completed"
                )
            else:
                self.cognitive_state.set_status(
                    "responded"
                )
        else:
            self.cognitive_state.set_status(
                "failed"
            )

        self.working_memory.add_observation(
            {
                "type": "brain_result",
                "success": result.success,
                "executed": result.executed,
                "response": result.response,
            }
        )

        result.metadata.setdefault(
            "cognitive_state",
            self.cognitive_state.snapshot(),
        )

        result.metadata.setdefault(
            "working_memory",
            self.working_memory.snapshot(),
        )

    # ------------------------------------------------------------------
    # Context
    # ------------------------------------------------------------------

    def _build_context(
        self,
        *,
        user_input: str,
        session_context: Any,
    ) -> Any:
        """
        Build cognitive context when a context manager is connected.
        """

        if self.context_manager is None:
            return None

        manager = self.context_manager

        if hasattr(manager, "build"):
            try:
                return manager.build(
                    user_input=user_input,
                    session_context=session_context,
                )
            except TypeError:
                try:
                    return manager.build(
                        user_input,
                        session_context,
                    )
                except TypeError:
                    return manager.build(
                        user_input
                    )

        if callable(manager):
            return manager(
                user_input
            )

        return None

    def _record_context(
        self,
        context: Any,
    ) -> None:
        """
        Record useful context information in working memory.
        """

        if context is None:
            return

        self.working_memory.add_fact(
            {
                "type": "cognitive_context",
                "value": context,
            }
        )

    # ------------------------------------------------------------------
    # Cognition
    # ------------------------------------------------------------------

    def _make_decision(
        self,
        *,
        user_input: str,
        context: Any,
    ) -> Any:
        """
        Ask the cognitive core for a decision.
        """

        if self.cognitive_core is None:
            raise RuntimeError(
                "Cognitive core is not connected."
            )

        core = self.cognitive_core

        if hasattr(core, "decide"):
            try:
                return core.decide(
                    user_input=user_input,
                    context=context,
                )
            except TypeError:
                try:
                    return core.decide(
                        user_input,
                        context,
                    )
                except TypeError:
                    return core.decide(
                        user_input
                    )

        if hasattr(core, "process"):
            try:
                return core.process(
                    user_input=user_input,
                    context=context,
                )
            except TypeError:
                try:
                    return core.process(
                        user_input,
                        context,
                    )
                except TypeError:
                    return core.process(
                        user_input
                    )

        if callable(core):
            return core(
                user_input
            )

        raise AttributeError(
            "Cognitive core does not provide "
            "a supported decision method."
        )

    # ------------------------------------------------------------------
    # Decision helpers
    # ------------------------------------------------------------------

    def _decision_type(
        self,
        decision: Any,
    ) -> str:
        """
        Normalize a cognitive decision type.
        """

        value = getattr(
            decision,
            "decision_type",
            None,
        )

        if value is None:
            value = getattr(
                decision,
                "type",
                None,
            )

        if hasattr(value, "value"):
            value = value.value

        if value is None:
            return ""

        return str(
            value
        ).strip().lower()

    # ------------------------------------------------------------------
    # Conversation
    # ------------------------------------------------------------------

    def _handle_conversation(
        self,
        decision: Any,
    ) -> BrainResult:
        response = getattr(
            decision,
            "response",
            "",
        )

        if not response:
            response = getattr(
                decision,
                "reasoning",
                "",
            )

        return BrainResult(
            success=True,
            response=str(
                response
            ),
            executed=False,
            decision=decision,
        )

    # ------------------------------------------------------------------
    # Clarification
    # ------------------------------------------------------------------

    def _handle_clarification(
        self,
        decision: Any,
    ) -> BrainResult:
        question = getattr(
            decision,
            "clarification_question",
            "",
        )

        if not question:
            question = getattr(
                decision,
                "response",
                "",
            )

        return BrainResult(
            success=True,
            response=str(
                question
            ),
            executed=False,
            decision=decision,
        )

    # ------------------------------------------------------------------
    # Refusal
    # ------------------------------------------------------------------

    def _handle_refusal(
        self,
        decision: Any,
    ) -> BrainResult:
        response = getattr(
            decision,
            "response",
            "",
        )

        if not response:
            response = (
                "ARES cannot perform "
                "that request."
            )

        return BrainResult(
            success=True,
            response=str(
                response
            ),
            executed=False,
            decision=decision,
        )

    # ------------------------------------------------------------------
    # Planning
    # ------------------------------------------------------------------

    def _handle_plan(
        self,
        *,
        decision: Any,
        user_input: str,
        context: Any,
    ) -> BrainResult:
        if self.planner is None:
            return BrainResult(
                success=True,
                response=(
                    "ARES created a plan but "
                    "no planner is currently connected."
                ),
                executed=False,
                decision=decision,
                metadata={
                    "plan": None,
                },
            )

        try:
            if hasattr(
                self.planner,
                "create_plan",
            ):
                plan = self.planner.create_plan(
                    user_input,
                    decision,
                )

            elif hasattr(
                self.planner,
                "plan",
            ):
                plan = self.planner.plan(
                    user_input,
                    decision,
                )

            elif callable(
                self.planner
            ):
                plan = self.planner(
                    user_input
                )

            else:
                raise AttributeError(
                    "Planner does not provide "
                    "a supported planning method."
                )

            self.cognitive_state.set_plan(
                plan
            )

            self.working_memory.add_fact(
                {
                    "type": "active_plan",
                    "value": plan,
                }
            )

            return BrainResult(
                success=True,
                response="Plan created.",
                executed=False,
                decision=decision,
                execution_result=plan,
                metadata={
                    "plan": plan,
                },
            )

        except Exception as exc:
            logger.exception(
                "Planning failed."
            )

            self.cognitive_state.record_failure()

            self.working_memory.add_observation(
                {
                    "type": "planning_failure",
                    "error": str(exc),
                }
            )

            return BrainResult(
                success=False,
                response=(
                    "ARES could not create "
                    "the requested plan."
                ),
                executed=False,
                decision=decision,
                error=str(exc),
            )

    # ------------------------------------------------------------------
    # Tool execution
    # ------------------------------------------------------------------

    def _handle_tool(
        self,
        *,
        decision: Any,
        user_input: str,
        context: Any,
    ) -> BrainResult:
        action = getattr(
            decision,
            "tool_name",
            None,
        )

        if action is None:
            action = getattr(
                decision,
                "action",
                None,
            )

        arguments = getattr(
            decision,
            "tool_arguments",
            None,
        )

        if arguments is None:
            arguments = getattr(
                decision,
                "arguments",
                {},
            )

        if arguments is None:
            arguments = {}

        if not isinstance(
            arguments,
            dict,
        ):
            arguments = dict(
                arguments
            )

        if not action:
            return BrainResult(
                success=False,
                response=(
                    "ARES received a tool "
                    "decision without a tool name."
                ),
                executed=False,
                decision=decision,
                error="Missing tool name.",
            )

        self.cognitive_state.set_status(
            "executing"
        )

        self.working_memory.add_pending_action(
            {
                "tool": action,
                "arguments": arguments,
            }
        )

        try:
            result = self._execute_tool(
                action=action,
                arguments=arguments,
                context=context,
            )

            self.cognitive_state.set_tool_result(
                result
            )

            self.working_memory.remove_pending_action(
                {
                    "tool": action,
                    "arguments": arguments,
                }
            )

            self.working_memory.add_observation(
                {
                    "type": "tool_result",
                    "tool": action,
                    "result": result,
                }
            )

        except Exception as exc:
            logger.exception(
                "Tool execution failed."
            )

            self.cognitive_state.record_failure()

            self.working_memory.remove_pending_action(
                {
                    "tool": action,
                    "arguments": arguments,
                }
            )

            self.working_memory.add_observation(
                {
                    "type": "tool_failure",
                    "tool": action,
                    "error": str(exc),
                }
            )

            return BrainResult(
                success=False,
                response=(
                    f"ARES could not execute "
                    f"'{action}'."
                ),
                executed=True,
                decision=decision,
                error=str(exc),
            )

        verification = self._verify(
            action=action,
            result=result,
        )

        self.cognitive_state.add_observation(
            {
                "type": "verification",
                "verified": getattr(
                    verification,
                    "verified",
                    False,
                ),
                "reason": self._verification_reason(
                    verification
                ),
            }
        )

        verified = bool(
            getattr(
                verification,
                "verified",
                True,
            )
        )

        if not verified:
            self.cognitive_state.record_failure()

        reflection = self._reflect(
            user_input=user_input,
            action=action,
            result=result,
            verification=verification,
            success=verified,
        )

        self.cognitive_state.set_status(
            "completed"
            if verified
            else "failed"
        )

        response = self._build_tool_response(
            action=action,
            success=verified,
            verification=verification,
        )

        return BrainResult(
            success=verified,
            response=response,
            executed=True,
            decision=decision,
            execution_result=result,
            verification=verification,
            reflection=reflection,
            error=""
            if verified
            else self._verification_reason(
                verification
            ),
            metadata={
                "cognitive_state": (
                    self.cognitive_state.snapshot()
                ),
                "working_memory": (
                    self.working_memory.snapshot()
                ),
            },
        )

    # ------------------------------------------------------------------
    # Tool execution compatibility
    # ------------------------------------------------------------------

    def _execute_tool(
        self,
        *,
        action: str,
        arguments: dict[str, Any],
        context: Any,
    ) -> Any:
        if self.orchestrator is None:
            raise RuntimeError(
                "No orchestrator is connected."
            )

        orchestrator = self.orchestrator

        if hasattr(
            orchestrator,
            "execute_tool",
        ):
            try:
                return orchestrator.execute_tool(
                    action,
                    arguments,
                )
            except TypeError:
                return orchestrator.execute_tool(
                    action=action,
                    arguments=arguments,
                )

        if hasattr(
            orchestrator,
            "execute",
        ):
            try:
                return orchestrator.execute(
                    action,
                    arguments,
                )
            except TypeError:
                try:
                    return orchestrator.execute(
                        action=action,
                        arguments=arguments,
                    )
                except TypeError:
                    return orchestrator.execute(
                        action,
                        arguments,
                        context,
                    )

        if hasattr(
            orchestrator,
            "run",
        ):
            try:
                return orchestrator.run(
                    action,
                    arguments,
                )
            except TypeError:
                return orchestrator.run(
                    action=action,
                    arguments=arguments,
                )

        if callable(
            orchestrator
        ):
            return orchestrator(
                action,
                arguments,
            )

        raise AttributeError(
            "Orchestrator does not provide "
            "a supported execution method."
        )

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def _verify(
        self,
        *,
        action: str,
        result: Any,
    ) -> Any:
        if self.verification_engine is None:
            return _FallbackVerification()

        engine = self.verification_engine

        if hasattr(
            engine,
            "verify",
        ):
            try:
                return engine.verify(
                    action=action,
                    result=result,
                )
            except TypeError:
                try:
                    return engine.verify(
                        action,
                        result,
                    )
                except TypeError:
                    return engine.verify(
                        result
                    )

        if callable(engine):
            try:
                return engine(
                    action,
                    result,
                )
            except TypeError:
                return engine(
                    result
                )

        return _FallbackVerification()

    # ------------------------------------------------------------------
    # Reflection
    # ------------------------------------------------------------------

    def _reflect(
        self,
        *,
        user_input: str,
        action: str,
        result: Any,
        verification: Any,
        success: bool,
    ) -> Any:
        if self.reflection_engine is None:
            return None

        engine = self.reflection_engine

        if hasattr(
            engine,
            "reflect",
        ):
            try:
                return engine.reflect()
            except TypeError:
                pass

        if callable(engine):
            try:
                return engine()
            except TypeError:
                return engine(
                    result
                )

        return None

    # ------------------------------------------------------------------
    # Response construction
    # ------------------------------------------------------------------

    def _build_tool_response(
        self,
        *,
        action: str,
        success: bool,
        verification: Any,
    ) -> str:
        if success:
            return "Action completed."

        reason = self._verification_reason(
            verification
        )

        if reason:
            return (
                f"ARES could not complete "
                f"'{action}': {reason}"
            )

        return (
            f"ARES could not complete "
            f"'{action}'."
        )

    def _verification_reason(
        self,
        verification: Any,
    ) -> str:
        reason = getattr(
            verification,
            "reason",
            "",
        )

        if reason:
            return str(reason)

        if isinstance(
            verification,
            dict,
        ):
            return str(
                verification.get(
                    "reason",
                    verification.get(
                        "error",
                        "",
                    ),
                )
            )

        return ""

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------

    def _record_working_memory(
        self,
        *,
        fact: Any,
    ) -> None:
        self.working_memory.add_fact(
            fact
        )

    def _store_memory(
        self,
        *,
        user_input: str,
        result: BrainResult,
    ) -> None:
        if self.memory_bridge is None:
            return

        bridge = self.memory_bridge

        try:
            if hasattr(
                bridge,
                "remember",
            ):
                bridge.remember(
                    user_input=user_input,
                    response=result.response,
                    decision=result.decision,
                    result=result.execution_result,
                    context=result.metadata,
                )
                return

            if hasattr(
                bridge,
                "store",
            ):
                bridge.store(
                    user_input,
                    result.response,
                )
                return

            if callable(bridge):
                bridge(
                    user_input,
                    result.response,
                )

        except Exception:
            logger.exception(
                "Long-term memory update failed."
            )


class _FallbackVerification:
    """
    Minimal verification result used when no verification
    engine is connected.

    This preserves compatibility with lightweight tests and
    development configurations.
    """

    verified = True

    reason = (
        "No verification engine was connected."
    )

    confidence = 0.5

    retryable = False