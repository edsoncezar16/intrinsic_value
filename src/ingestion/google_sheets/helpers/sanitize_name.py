import re


def sanitize_dagster_name(name: str) -> str:
    """
    Sanitize a string to be a valid Dagster name.

    Dagster names must match the regex: ^[A-Za-z0-9_]+$
    This function removes or replaces invalid characters.

    Args:
        name: The original name string

    Returns:
        A sanitized string that is valid for Dagster names
    """
    if not name:
        return "unnamed"

    # Replace hyphens with underscores (common case)
    sanitized = name.replace("-", "_")

    # Remove all non-alphanumeric characters except underscores
    sanitized = re.sub(r"[^A-Za-z0-9_]+", "", sanitized)

    # Ensure it doesn't start with a number (good practice)
    if sanitized and sanitized[0].isdigit():
        sanitized = f"_{sanitized}"

    # Handle empty result
    if not sanitized:
        return "unnamed"

    return sanitized
