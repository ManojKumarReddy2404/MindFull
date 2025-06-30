import json
from pathlib import Path

MEMORY_LOG_FILE = "memory_log.json"

def write_memory(entry: dict) -> None:
    """
    Write a memory entry to memory_log.json.
    Each entry is written as a new line for easy appending.
    """
    try:
        # Create the file if it doesn't exist
        if not Path(MEMORY_LOG_FILE).exists():
            with open(MEMORY_LOG_FILE, "w") as f:
                f.write("")  # Initialize empty file

        # Append the new entry
        with open(MEMORY_LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Warning: Failed to write to memory log: {str(e)}")

def read_memory() -> list:
    """
    Read all memory entries from memory_log.json.
    Returns a list of dictionaries.
    """
    try:
        if not Path(MEMORY_LOG_FILE).exists():
            return []

        entries = []
        with open(MEMORY_LOG_FILE, "r") as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    entries.append(json.loads(line))
        return entries
    except Exception as e:
        print(f"Warning: Failed to read memory log: {str(e)}")
        return [] 