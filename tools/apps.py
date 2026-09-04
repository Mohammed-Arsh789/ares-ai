import subprocess


ALLOWED_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
}


def launch_app(name):

    name = name.lower().strip()

    if name not in ALLOWED_APPS:
        raise ValueError(
            f"Application '{name}' is not allowed."
        )

    subprocess.Popen(
        ALLOWED_APPS[name]
    )

    return f"Launched {name}."