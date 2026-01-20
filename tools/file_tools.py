from pathlib import Path
import shutil
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


@tool
def copy_file(source: str, destination: str) -> str:
    """Copy a file from source path to destination path.

    Args:
        source: Source file path.
        destination: Destination file path.

    Returns:
        Success message or error message.
    """
    try:
        if not Path(source).exists():
            return f"Error: Source file not found at {source}"
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return f"Successfully copied {source} to {destination}"
    except PermissionError as e:
        return f"Error copying file: Permission denied - {str(e)}"
    except Exception as e:
        return f"Error copying file: {str(e)}"


@tool
def delete_file(path: str) -> str:
    """Delete a file at the given path.

    Args:
        path: Absolute or relative path to the file.

    Returns:
        Success message or error message.
    """
    try:
        if not Path(path).exists():
            return f"Error: File not found at {path}"
        Path(path).unlink()
        return f"Successfully deleted {path}"
    except PermissionError as e:
        return f"Error deleting file: Permission denied - {str(e)}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"


@tool
def search_files(directory: str = ".", pattern: str = "*") -> str:
    """Search for files matching a glob pattern in a directory.

    Args:
        directory: Directory path to search in (defaults to current directory).
        pattern: Glob pattern to match (e.g., "*.txt", "*.py", "test*").

    Returns:
        Formatted list of matching files with metadata (size, type).
    """
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return f"Error: Directory not found at {directory}"

        matches = list(dir_path.glob(pattern))
        if not matches:
            return f"No files found matching pattern {pattern} in {directory}"

        results = []
        for match in matches:
            size = match.stat().st_size
            file_type = "DIR" if match.is_dir() else "FILE"
            results.append(f"{file_type} {match.name} ({size} bytes)")

        return f"Found {len(matches)} files matching {pattern}:\n" + "\n".join(results)
    except Exception as e:
        return f"Error searching files: {str(e)}"
