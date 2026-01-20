from datetime import datetime
from langchain.tools import tool


@tool
def get_current_time() -> str:
    """Get the current date and time in ISO format.

    Returns:
        Current timestamp as string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def send_notification(message: str) -> str:
    """Send a notification message.

    Args:
        message: The notification text.

    Returns:
        Confirmation message.

    Note: Currently prints to console. Can be extended to Slack/Email.
    """
    print(f"[NOTIFICATION] {message}")
    return f"Notification sent: {message}"


@tool
def append_to_log(message: str, log_file: str = "agent.log") -> str:
    """Append a message with a timestamp to a log file.

    Args:
        message: Message to log.
        log_file: Path to the log file (default: agent.log).

    Returns:
        Confirmation message.
    """
    try:
        from pathlib import Path

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        Path(log_file).write_text(log_entry, encoding="utf-8")
        return f"Logged to {log_file}"
    except Exception as e:
        return f"Error logging message: {str(e)}"
