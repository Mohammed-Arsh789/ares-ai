from dataclasses import dataclass, field


@dataclass
class PluginMetadata:
    name: str
    version: str
    description: str = ""
    author: str = ""
    required_ares_version: str | None = None
    permissions: list[str] = field(
        default_factory=list
    )


@dataclass
class PluginState:
    enabled: bool = False
    loaded: bool = False
    error: str | None = None