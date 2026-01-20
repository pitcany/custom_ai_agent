from pathlib import Path
from langchain.tools import tool


@tool
def read_file(path: str) -> str:
    """Read contents of a file at the given path.

    Args:
        path: Absolute or relative path to the file.

    Returns:
        File contents as string or error message.
    """
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: File not found at {path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path.

    Args:
        path: Absolute or relative path to the file.
        content: Text content to write.

    Returns:
        Success message or error message.
    """
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content, encoding="utf-8")
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def list_directory(path: str = ".") -> str:
    """List all files and directories in the given path.

    Args:
        path: Directory path (defaults to current directory).

    Returns:
        Formatted list of files and directories.
    """
    try:
        items = list(Path(path).iterdir())
        return "\n".join(
            f"{'DIR  ' if item.is_dir() else 'FILE '}{item.name}"
            for item in sorted(items)
        )
    except FileNotFoundError:
        return f"Error: Directory not found at {path}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"
