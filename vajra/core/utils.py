import os
import shutil

from rich.console import Console

console = Console()

GO_BIN = os.path.expanduser("~/go/bin")


def tool_path(name):
    """Return usable command name/path for a tool, checking PATH and ~/go/bin."""

    if shutil.which(name):
        return name

    candidate = os.path.join(GO_BIN, name)

    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        return candidate

    return None


def require_tool(name):
    """Returns command path if available, else prints a warning and returns None."""

    path = tool_path(name)

    if path is None:
        console.print(
            f"[red][-] '{name}' not found — skipping this step. "
            f"Run VAJRA again to let it retry installing it.[/red]"
        )

    return path
