"""
ARES Memory Types
Step 162
"""

from enum import Enum


class MemoryType(str, Enum):

    GENERAL = "general"

    PERSONAL = "personal"

    PREFERENCE = "preference"

    PROJECT = "project"

    TASK = "task"

    KNOWLEDGE = "knowledge"

    CONVERSATION = "conversation"

    STUDY = "study"

    SYSTEM = "system"

    EPISODIC = "episodic"

    SEMANTIC = "semantic"