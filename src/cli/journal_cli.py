"""Secret Journal CLI App

Run from the project root with:
    python -m src.cli.journal_cli
"""

from src.api.utils.file_handler import add_entry, load_entries
from src.core.config import MAX_ENTRY_LENGTH, MOOD_SYMBOLS


def get_user_name() -> str:
    """Greet the user and return their name."""
    print("Welcome to the Secret Journal!")
    name = input("Enter your name: ").strip()
    print(f"\nHello {name}! Let's start journaling!\n")
    return name


def _read_message() -> str:
    """Keep prompting until the user provides a valid message."""
    while True:
        message = input("Write your journal message: ").strip()
        if not message:
            print("Message can't be empty. Please try again.\n")
        elif len(message) > MAX_ENTRY_LENGTH:
            print(f"Message can't exceed {MAX_ENTRY_LENGTH} characters.\n")
        else:
            return message


def _read_mood() -> str:
    """Keep prompting until the user picks a valid mood, return its ASCII symbol."""
    valid_moods = ", ".join(MOOD_SYMBOLS)
    while True:
        mood = input(f"How do you feel today? ({valid_moods}): ").strip().lower()
        if mood in MOOD_SYMBOLS:
            return MOOD_SYMBOLS[mood]
        print(f"'{mood}' isn't a valid mood. Choose one of: {valid_moods}.\n")


def display_entries(entries: list) -> None:
    """Print saved entries in a readable, bordered list."""
    if not entries:
        print("No journal entries yet. Write one first!\n")
        return

    print("------ Journal Entries ------")
    for entry in entries:
        print(
            f"{entry['id']} | {entry['mood']} | {entry['message']} "
            f"| {entry['timestamp']}"
        )
    print("-----------------------------\n")


def _print_menu() -> None:
    print("What would you like to do?")
    print("1. Write a new journal entry")
    print("2. View saved entries")
    print("3. Exit")


def main() -> None:
    """Run the Secret Journal CLI menu loop."""
    get_user_name()

    while True:
        _print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # The id is worked out at save time so CLI and API never clash.
            add_entry(_read_message(), _read_mood())
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
