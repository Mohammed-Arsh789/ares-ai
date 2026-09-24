from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BrainResult:
    """
    Final result returned by ARESBrain.process().
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
    Main coordination layer for ARES.

    Pipeline:

        User Input
            ↓
        Cognitive Core
            ↓
        Decision
            ↓
        Planner / Orchestrator
            ↓
        Tool Execution
            ↓
        Verification
            ↓
        Reflection
            ↓
        Response
    """

    def __init__(
        self,
        *,
        cognitive_core: Any,
        reflection_engine: Any = None,
        orchestrator: Any = None,
        planner: Any = None,
        context_manager: Any = None,
        memory_bridge: Any = None,
        verification_engine: Any = None,
        recovery_engine: Any = None,
    ) -> None:
        self.cognitive_core = cognitive_core
        self.reflection_engine = reflection_engine
        self.orchestrator = orchestrator
        self.planner = planner
        self.context_manager = context_manager
        self.memory_bridge = memory_bridge
        self.verification_engine = verification_engine
        self.recovery_engine = recovery_engine

    def process(
        self,
        user_input: str,
        *,
        session_context: dict[str, Any] | None = None,
    ) -> BrainResult:
        """
        Process one user request through the ARES cognitive pipeline.
        """

        if not isinstance(user_input, str):
            raise TypeError(
                "user_input must be a string."
            )

        if not user_input.strip():
            raise ValueError(
                "Cannot process empty input."
            )

        logger.info(
            "ARES processing input: %s",
            user_input,
        )

        try:
            context = self._build_context(
                user_input=user_input,
                session_context=session_context,
            )

            decision = self._make_decision(
                user_input=user_input,
                context=context,
            )

            return self._handle_decision(
                decision=decision,
                user_input=user_input,
                context=context,
            )

        except Exception as exc:
            logger.exception(
                "ARES brain processing failed."
            )

            return BrainResult(
                success=False,
                response=(
                    "ARES encountered an internal error."
                ),
                error=str(exc),
            )

    # =========================================================
    # CONTEXT
    # =========================================================

    def _build_context(
        self,
        *,
        user_input: str,
        session_context: dict[str, Any] | None,
    ) -> Any:
        """
        Build cognitive context when a context manager exists.
        """

        if self.context_manager is None:
            return None

        try:
            return self.context_manager.build(
                user_input=user_input,
                session_context=session_context or {},
            )

        except TypeError:
            try:
                return self.context_manager.build(
                    user_input,
                    session_context or {},
                )

            except TypeError:
                return self.context_manager.build(
                    user_input
                )

    # =========================================================
    # COGNITION
    # =========================================================

    def _make_decision(
        self,
        *,
        user_input: str,
        context: Any,
    ) -> Any:
        """
        Ask the Cognitive Core what ARES should do.
        """

        if hasattr(
            self.cognitive_core,
            "decide",
        ):
            try:
                return self.cognitive_core.decide(
                    user_input=user_input,
                    context=context,
                )

            except TypeError:
                try:
                    return self.cognitive_core.decide(
                        user_input,
                        context,
                    )

                except TypeError:
                    return self.cognitive_core.decide(
                        user_input
                    )

        if hasattr(
            self.cognitive_core,
            "process",
        ):
            try:
                return self.cognitive_core.process(
                    user_input=user_input,
                    context=context,
                )

            except TypeError:
                return self.cognitive_core.process(
                    user_input
                )

        raise AttributeError(
            "Cognitive core does not provide "
            "a supported decision method."
        )

    # =========================================================
    # DECISION ROUTING
    # =========================================================

    def _handle_decision(
        self,
        *,
        decision: Any,
        user_input: str,
        context: Any,
    ) -> BrainResult:
        """
        Route the cognitive decision.
        """

        decision_type = self._decision_type(
            decision
        )

        name = self._normalize_decision_type(
            decision_type
        )

        if name == "conversation":
            return self._handle_conversation(
                decision
            )

        if name == "clarification":
            return self._handle_clarification(
                decision
            )

        if name == "refuse":
            return self._handle_refusal(
                decision
            )

        if name == "plan":
            return self._handle_plan(
                decision=decision,
                user_input=user_input,
                context=context,
            )

        if name == "tool":
            return self._handle_tool(
                decision=decision,
                user_input=user_input,
                context=context,
            )

        logger.warning(
            "Unknown decision type: %s",
            decision_type,
        )

        return BrainResult(
            success=False,
            response=(
                "ARES could not determine what "
                "action to take."
            ),
            decision=decision,
        )

    def _decision_type(
        self,
        decision: Any,
    ) -> Any:
        if hasattr(
            decision,
            "decision_type",
        ):
            return decision.decision_type

        if hasattr(
            decision,
            "type",
        ):
            return decision.type

        if isinstance(
            decision,
            dict,
        ):
            return decision.get(
                "decision_type",
                decision.get("type"),
            )

        return None

    def _normalize_decision_type(
        self,
        value: Any,
    ) -> str:
        if value is None:
            return ""

        if hasattr(
            value,
            "value",
        ):
            value = value.value

        text = str(value).strip().lower()

        return (
            text
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
        )

    # =========================================================
    # CONVERSATION
    # =========================================================

    def _handle_conversation(
        self,
        decision: Any,
    ) -> BrainResult:
        response = self._decision_value(
            decision,
            "response",
            "",
        )

        return BrainResult(
            success=True,
            response=str(response),
            executed=False,
            decision=decision,
        )

    # =========================================================
    # CLARIFICATION
    # =========================================================

    def _handle_clarification(
        self,
        decision: Any,
    ) -> BrainResult:
        response = self._decision_value(
            decision,
            "clarification_question",
            None,
        )

        if not response:
            response = self._decision_value(
                decision,
                "response",
                "Could you clarify that?",
            )

        return BrainResult(
            success=True,
            response=str(response),
            executed=False,
            decision=decision,
        )

    # =========================================================
    # REFUSAL
    # =========================================================

    def _handle_refusal(
        self,
        decision: Any,
    ) -> BrainResult:
        response = self._decision_value(
            decision,
            "response",
            "ARES cannot help with that request.",
        )

        return BrainResult(
            success=True,
            response=str(response),
            executed=False,
            decision=decision,
        )

    # =========================================================
    # PLAN
    # =========================================================

    def _handle_plan(
        self,
        *,
        decision: Any,
        user_input: str,
        context: Any,
    ) -> BrainResult:
        """
        Send planning decisions to the connected planner.
        """

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

            return BrainResult(
                success=False,
                response="ARES could not create the plan.",
                executed=False,
                decision=decision,
                error=str(exc),
            )

    # =========================================================
    # TOOL EXECUTION
    # =========================================================

    def _handle_tool(
        self,
        *,
        decision: Any,
        user_input: str,
        context: Any,
    ) -> BrainResult:
        """
        Execute a tool through the orchestrator.
        """

        action = self._decision_value(
            decision,
            "tool_name",
            None,
        )

        arguments = self._decision_value(
            decision,
            "tool_arguments",
            {},
        )

        if not action:
            return BrainResult(
                success=False,
                response=(
                    "ARES selected a tool but "
                    "did not specify which tool."
                ),
                executed=False,
                decision=decision,
            )

        if arguments is None:
            arguments = {}

        if not isinstance(
            arguments,
            dict,
        ):
            arguments = dict(arguments)

        if self.orchestrator is None:
            return BrainResult(
                success=False,
                response=(
                    f"ARES selected '{action}', "
                    "but no orchestrator is connected."
                ),
                executed=False,
                decision=decision,
            )

        try:
            result = self._execute_tool(
                action=action,
                arguments=arguments,
                context=context,
            )

        except Exception as exc:
            logger.exception(
                "Tool execution failed: %s",
                action,
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

        success = self._verification_success(
            verification=verification,
            result=result,
        )

        reflection = self._reflect(
            user_input=user_input,
            action=action,
            result=result,
            verification=verification,
            success=success,
        )

        final_success = self._reflection_success(
            reflection=reflection,
            fallback=success,
        )

        response = self._build_tool_response(
            action=action,
            result=result,
            verification=verification,
            success=final_success,
            reflection=reflection,
        )

        self._remember(
            user_input=user_input,
            response=response,
            decision=decision,
            result=result,
            context=context,
        )

        return BrainResult(
            success=final_success,
            response=response,
            executed=True,
            decision=decision,
            execution_result=result,
            verification=verification,
            reflection=reflection,
        )

    def _execute_tool(
        self,
        *,
        action: str,
        arguments: dict[str, Any],
        context: Any,
    ) -> Any:
        """
        Execute a tool through the connected orchestrator.
        """

        if hasattr(
            self.orchestrator,
            "execute_tool",
        ):
            try:
                return self.orchestrator.execute_tool(
                    action,
                    arguments,
                )

            except TypeError:
                return self.orchestrator.execute_tool(
                    action=action,
                    arguments=arguments,
                )

        if hasattr(
            self.orchestrator,
            "execute",
        ):
            try:
                return self.orchestrator.execute(
                    action,
                    arguments,
                )

            except TypeError:
                try:
                    return self.orchestrator.execute(
                        action=action,
                        arguments=arguments,
                    )

                except TypeError:
                    return self.orchestrator.execute(
                        action,
                        arguments,
                        context,
                    )

        if hasattr(
            self.orchestrator,
            "run",
        ):
            try:
                return self.orchestrator.run(
                    action,
                    arguments,
                )

            except TypeError:
                return self.orchestrator.run(
                    action=action,
                    arguments=arguments,
                )

        if callable(
            self.orchestrator
        ):
            return self.orchestrator(
                action,
                arguments,
            )

        raise AttributeError(
            "Orchestrator does not provide "
            "a supported execution method."
        )

    # =========================================================
    # VERIFICATION
    # =========================================================

    def _verify(
        self,
        *,
        action: str,
        result: Any,
    ) -> Any:
        if self.verification_engine is None:
            return None

        verifier = self.verification_engine

        if hasattr(
            verifier,
            "verify",
        ):
            try:
                return verifier.verify(
                    action=action,
                    result=result,
                )

            except TypeError:
                return verifier.verify(
                    action,
                    result,
                )

        if callable(verifier):
            return verifier(
                action,
                result,
            )

        return None

    def _verification_success(
        self,
        *,
        verification: Any,
        result: Any,
    ) -> bool:
        if verification is None:
            return True

        if hasattr(
            verification,
            "verified",
        ):
            return bool(
                verification.verified
            )

        if hasattr(
            verification,
            "success",
        ):
            return bool(
                verification.success
            )

        if isinstance(
            verification,
            dict,
        ):
            if "verified" in verification:
                return bool(
                    verification["verified"]
                )

            if "success" in verification:
                return bool(
                    verification["success"]
                )

        return True

    def _verification_reason(
        self,
        verification: Any,
    ) -> str:
        if verification is None:
            return ""

        if hasattr(
            verification,
            "reason",
        ):
            return str(
                verification.reason or ""
            )

        if isinstance(
            verification,
            dict,
        ):
            return str(
                verification.get(
                    "reason",
                    "",
                )
            )

        return ""

    # =========================================================
    # REFLECTION
    # =========================================================

    def _reflect(
        self,
        *,
        user_input: str,
        action: str,
        result: Any,
        verification: Any,
        success: bool,
    ) -> Any:
        """
        Run the reflection engine.
        """

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

    def _reflection_success(
        self,
        *,
        reflection: Any,
        fallback: bool,
    ) -> bool:
        if reflection is None:
            return fallback

        if hasattr(
            reflection,
            "success",
        ):
            return bool(
                reflection.success
            )

        if isinstance(
            reflection,
            dict,
        ) and "success" in reflection:
            return bool(
                reflection["success"]
            )

        return fallback

    # =========================================================
    # RESPONSE
    # =========================================================

    def _build_tool_response(
        self,
        *,
        action: str,
        result: Any,
        verification: Any,
        success: bool,
        reflection: Any,
    ) -> str:
        """
        Convert a verified tool execution
        into a user-facing response.
        """

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
            f"ARES could not complete '{action}'."
        )

    # =========================================================
    # MEMORY
    # =========================================================

    def _remember(
        self,
        *,
        user_input: str,
        response: str,
        decision: Any,
        result: Any,
        context: Any,
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
                    response=response,
                    decision=decision,
                    result=result,
                    context=context,
                )
                return

            if hasattr(
                bridge,
                "store",
            ):
                bridge.store(
                    user_input=user_input,
                    response=response,
                    decision=decision,
                    result=result,
                    context=context,
                )
                return

        except Exception:
            logger.exception(
                "Memory update failed."
            )

    # =========================================================
    # GENERIC HELPERS
    # =========================================================

    def _decision_value(
        self,
        decision: Any,
        name: str,
        default: Any,
    ) -> Any:
        if hasattr(
            decision,
            name,
        ):
            value = getattr(
                decision,
                name,
            )

            if value is not None:
                return value

        if isinstance(
            decision,
            dict,
        ):
            return decision.get(
                name,
                default,
            )

        return default