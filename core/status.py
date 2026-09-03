class ARESStatus:
    def __init__(self, ares):
        self.ares = ares

    def report(self):
        return {
            "ai": self._check_ai(),
            "memory": self._check_memory(),
            "tools": self._check_tools(),
            "voice": self._check_voice(),
            "vision": self._check_vision(),
        }

    def _check_ai(self):
        return self.ares.ai is not None

    def _check_memory(self):
        return self.ares.memory is not None

    def _check_tools(self):
        return len(
            self.ares.tools.available_tools()
        ) > 0

    def _check_voice(self):
        try:
            import pyttsx3
            return True
        except ImportError:
            return False

    def _check_vision(self):
        try:
            import cv2
            return True
        except ImportError:
            return False