"""Secret Journal CLI App"""

import csv
from pathlib import Path
from datetime import datetime

JOURNAL_FILE = Path(__file__).parent / "journal.csv"
CSV_FIELDS = ["id", "message", "mood", "timestamp"]

# Maps a mood keyword to the ASCII face stored in the CSV.
MOOD_SYMBOLS = {
    "happy": ":)",
    "sad": ":(",
    "neutral": ":|",
}


def get_user_name() -> str:
    """Greet the user and return their name."""
    print("Welcome to the Secret Journal!")
    name = input("Enter your name: ").strip()
    print(f"\nHello {name}! Let's start journaling!\n")
    return name


def _read_message() -> str:
    """Keep prompting until the user provides a non-empty message."""
    while True:
        message = input("Write your journal message: ").strip()
        if message:
            return message
        print("Message can't be empty. Please try again.\n")


def _read_mood() -> str:
    """Keep prompting until the user picks a valid mood, return its ASCII symbol."""
    valid_moods = ", ".join(MOOD_SYMBOLS)
    while True:
        mood = input(f"How do you feel today? ({valid_moods}): ").strip().lower()
        if mood in MOOD_SYMBOLS:
            return MOOD_SYMBOLS[mood]
        print(f"'{mood}' isn't a valid mood. Choose one of: {valid_moods}.\n")


def create_entry(entry_id: int) -> dict:
    """Collect and validate user input, returning a new journal entry."""
    message = _read_message()
    mood = _read_mood()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "id": entry_id,
        "message": message,
        "mood": mood,
        "timestamp": timestamp,
    }


def save_entry_to_csv(entry: dict) -> None:
    """Append a single entry to the journal CSV, writing a header if new."""
    is_new_file = not JOURNAL_FILE.exists()

    with open(JOURNAL_FILE, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(entry)


def load_entries() -> list:
    """Read all saved entries from the CSV file, oldest first."""
    if not JOURNAL_FILE.exists():
        return []

    with open(JOURNAL_FILE, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def display_entries(entries: list) -> None:
    """Print saved entries in a readable, bordered list."""
    if not entries:
        print("No journal entries yet. Write one first!\n")
        return

    print("------ Journal Entries ------")
    for entry in entries:
        print(f"{entry['id']} | {entry['mood']} | {entry['message']} | {entry['timestamp']}")
    print("-----------------------------\n")


def _next_entry_id(entries: list) -> int:
    """Work out the next auto-incrementing id from existing entries."""
    if not entries:
        return 1
    return max(int(entry["id"]) for entry in entries) + 1


def _print_menu() -> None:
    print("What would you like to do?")
    print("1. Write a new journal entry")
    print("2. View saved entries")
    print("3. Exit")


def main() -> None:
    """Run the Secret Journal CLI menu loop."""
    get_user_name()
    entries = load_entries()
    next_id = _next_entry_id(entries)

    while True:
        _print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            entry = create_entry(next_id)
            save_entry_to_csv(entry)
            next_id += 1
            print("Entry saved!\n")
        elif choice == "2":
            display_entries(load_entries())
        elif choice == "3":
            print("Goodbye! Keep journaling.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye! Keep journaling.")
