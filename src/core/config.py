"""Central configuration shared by the CLI and the API."""

from pathlib import Path

# Project root is three levels up: src/core/config.py -> src/core -> src -> root
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
JOURNAL_FILE = DATA_DIR / "journal.csv"

# Column order of the journal CSV (unchanged from Day 1).
CSV_FIELDS = ["id", "message", "mood", "timestamp"]
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

# Maximum number of characters allowed in a single journal entry.
MAX_ENTRY_LENGTH = 500

# Mood keyword -> ASCII face stored in the CSV "mood" column (Day 1 format).
MOOD_SYMBOLS = {
    "happy": ":)",
    "sad": ":(",
    "neutral": ":|",
}

# Mood keyword -> sentiment label used by the GET /journal filter.
MOOD_SENTIMENTS = {
    "happy": "positive",
    "sad": "negative",
    "neutral": "neutral",
}

# Origins allowed to call the API from a browser. "*" keeps local development
# simple (it also covers frontend.html opened straight from disk, whose origin
# is "null"). Narrow this to real frontend URLs before deploying.
CORS_ORIGINS = ["*"]

API_TITLE = "Secret Journal API"
API_DESCRIPTION = "Write and read journal entries, each tagged with a mood."
API_VERSION = "2.0.0"
