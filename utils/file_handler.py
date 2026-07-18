"""JSON file read/write helpers for the retail sales analytics platform."""

import json
import os
from typing import Any, List, Dict

from utils.logger import get_logger

logger = get_logger(__name__)


def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Load a JSON file and return its contents as a list of dicts.

    If the file does not exist or is empty, an empty list is returned
    instead of raising, so first-time runs work without setup.

    Args:
        file_path: Path to the JSON file to load.

    Returns:
        The parsed JSON content as a list of dictionaries.

    Raises:
        json.JSONDecodeError: If the file exists but contains invalid JSON.
    """
    if not os.path.exists(file_path):
        logger.warning("File not found, starting with empty data: %s", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error("Corrupted JSON in %s: %s", file_path, exc)
        raise


def save_json(file_path: str, data: List[Dict[str, Any]]) -> None:
    """Save a list of dicts to a JSON file, creating parent folders if needed.

    Args:
        file_path: Path to the JSON file to write.
        data: The data to serialize as JSON.
    """
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logger.info("Saved %d record(s) to %s", len(data), file_path)
