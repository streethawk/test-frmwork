from __future__ import annotations

import subprocess


def run_pipeline(trigger_cmd: list[str]) -> None:
    completed = subprocess.run(trigger_cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "Pipeline execution failed:\n"
            f"Command: {' '.join(trigger_cmd)}\n"
            f"stdout: {completed.stdout}\n"
            f"stderr: {completed.stderr}"
        )
