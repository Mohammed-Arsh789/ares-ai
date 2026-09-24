from __future__ import annotations

import json
import logging
from typing import Any, Protocol
from urllib import request


logger = logging.getLogger(__name__)


class ModelProvider(Protocol):
    """
    Interface implemented by an LLM backend.
    """

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
    ) -> str:
        ...


class OllamaProvider:
    """
    Lightweight Ollama model provider.

    Uses Python's standard library so ARES does not need another
    dependency just to communicate with the local Ollama server.
    """

    def __init__(
        self,
        model: str = "qwen2.5:1.5b",
        host: str = "http://127.0.0.1:11434",
        timeout: float = 120.0,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        data = json.dumps(payload).encode("utf-8")

        req = request.Request(
            f"{self.host}/api/generate",
            data=data,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(
                req,
                timeout=self.timeout,
            ) as response:
                raw = response.read().decode("utf-8")

            result = json.loads(raw)

        except Exception as exc:
            logger.exception("Ollama generation failed")
            raise RuntimeError(
                f"Ollama generation failed: {exc}"
            ) from exc

        output = result.get("response")

        if not isinstance(output, str):
            raise RuntimeError(
                "Ollama returned an invalid response."
            )

        return output.strip()


class ModelRouter:
    """
    Routes cognitive requests to the configured model provider.

    Keeping this separate allows future model routing such as:

        fast model → simple tasks
        reasoning model → complex tasks
        vision model → images
        coding model → programming
    """

    def __init__(
        self,
        provider: ModelProvider | None = None,
    ) -> None:
        self.provider = provider or OllamaProvider()

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
    ) -> str:
        return self.provider.generate(
            prompt,
            system=system,
        )