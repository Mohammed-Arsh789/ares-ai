import subprocess


ALLOWED_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "paint": ["mspaint.exe"],
    "command prompt": ["cmd.exe"],
    "cmd": ["cmd.exe"],
}


def launch_app(name):
    """
    Launch an explicitly allowlisted Windows application.
    """

    name = name.lower().strip()

    if name not in ALLOWED_APPS:
        raise ValueError(
            f"Application '{name}' is not allowed."
        )

    subprocess.Popen(
        ALLOWED_APPS[name],
        shell=False
    )

    return f"Launched {name}."