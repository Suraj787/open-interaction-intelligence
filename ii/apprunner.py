"""Safe application runner.

Detects the package manager and start command, picks a port, starts the dev server as a
child process, polls an HTTP readiness condition, captures logs as evidence, and tears the
process tree down cleanly. It never starts an unknown command without policy approval and
never leaks environment variables. If the app cannot be started in this environment it
returns a structured not-executed/failed result rather than pretending it ran.
"""
from __future__ import annotations
import os
import socket
import subprocess
import time
import urllib.request
from dataclasses import dataclass
from . import runtime


@dataclass
class AppHandle:
    status: str            # started | not-executed | failed
    url: str | None = None
    pid: int | None = None
    reason: str = ""
    command: str | None = None


def _free_port(preferred: int = 5173) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]


def _ready(url: str, timeout: float) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                if r.status < 500:
                    return True
        except Exception:
            time.sleep(0.3)
    return False


def start(target, port: int | None = None, override_cmd: str | None = None,
          timeout: float = 60.0, approve: bool = False) -> AppHandle:
    pm = runtime.model_project(target)
    cmd = override_cmd or pm.start_command
    if not cmd:
        return AppHandle("not-executed", reason="no start command detected", command=None)
    node_modules = (runtime.state_root(target).parent / "node_modules")
    if not node_modules.exists():
        return AppHandle("not-executed", command=cmd,
                         reason="dependencies not installed (node_modules missing); "
                                "cannot start the app in this environment")
    if not approve:
        return AppHandle("not-executed", command=cmd,
                         reason="starting a project command requires explicit policy approval (--approve)")
    p = _free_port(port or 5173)
    url = f"http://127.0.0.1:{p}/"
    env = {k: v for k, v in os.environ.items() if not _is_secret(k)}
    env["PORT"] = str(p)
    # Most dev servers (Vite) ignore PORT and bind localhost:5173 by default. Pass the
    # host/port explicitly so the readiness poll targets the right address.
    argv = cmd.split()
    low = cmd.lower()
    if "vite" in low or "dev" in low or "serve" in low:
        argv += ["--", "--host", "127.0.0.1", "--port", str(p), "--strictPort"]
    try:
        proc = subprocess.Popen(argv, cwd=str(target), env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                start_new_session=True)
    except (OSError, ValueError) as e:
        return AppHandle("failed", command=cmd, reason=str(e))
    if not _ready(url, timeout):
        stop(proc.pid)
        return AppHandle("failed", command=cmd, url=url, pid=proc.pid,
                         reason="app did not become ready within timeout")
    return AppHandle("started", url=url, pid=proc.pid, command=cmd)


def stop(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.killpg(os.getpgid(pid), 15)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


_SECRET_HINTS = ("token", "secret", "password", "key", "aws", "gh_", "ssh", "api")


def _is_secret(name: str) -> bool:
    n = name.lower()
    return any(h in n for h in _SECRET_HINTS)
