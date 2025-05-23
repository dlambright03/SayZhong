"""Core functionality for SayZhong."""


def greet(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message.
    """
    return f"你好, {name}!"


def calculate_learning_progress(completed_lessons: int, total_lessons: int) -> float:
    """Calculate learning progress percentage.

    Args:
        completed_lessons: Number of completed lessons.
        total_lessons: Total number of lessons.

    Returns:
        Progress as a percentage (0.0 to 100.0).

    Raises:
        ValueError: If total_lessons is 0 or negative.
    """
    if total_lessons <= 0:
        raise ValueError("Total lessons must be positive")

    return (completed_lessons / total_lessons) * 100.0
