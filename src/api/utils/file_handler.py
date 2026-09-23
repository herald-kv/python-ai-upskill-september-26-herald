"""CSV storage for journal entries, shared by the CLI and the API."""

import csv
from datetime import datetime

from src.core.config import CSV_FIELDS, JOURNAL_FILE, TIMESTAMP_FORMAT


def load_entries() -> list[dict]:
    """Read all saved entries from the CSV file, oldest first."""
    if not JOURNAL_FILE.exists():
        return []

    with open(JOURNAL_FILE, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def save_entry(entry: dict) -> None:
    """Append a single entry to the journal CSV, writing a header if new."""
    JOURNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    is_new_file = not JOURNAL_FILE.exists()

    with open(JOURNAL_FILE, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(entry)


def next_entry_id(entries: list[dict]) -> int:
    """Work out the next auto-incrementing id from existing entries."""
    if not entries:
        return 1
    return max(int(entry["id"]) for entry in entries) + 1


def add_entry(message: str, mood: str) -> dict:
    """Build a new entry with the next id and current time, save it, return it."""
    entry = {
        "id": next_entry_id(load_entries()),
        "message": message,
        "mood": mood,
        "timestamp": datetime.now().strftime(TIMESTAMP_FORMAT),
    }
    save_entry(entry)
    return entry
