"""Pydantic models describing journal API requests and responses."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator

from src.core.config import MAX_ENTRY_LENGTH, MOOD_SENTIMENTS, MOOD_SYMBOLS


class Mood(str, Enum):
    """Moods a user can pick, same choices as the Day 1 CLI."""

    happy = "happy"
    sad = "sad"
    neutral = "neutral"


class Sentiment(str, Enum):
    """Allowed values for the GET /journal sentiment filter."""

    positive = "positive"
    negative = "negative"
    neutral = "neutral"


# Reverse lookup so a stored ASCII face can be turned back into a mood keyword.
SYMBOL_TO_MOOD = {symbol: mood for mood, symbol in MOOD_SYMBOLS.items()}


class JournalEntryCreate(BaseModel):
    """Request body for POST /journal."""

    entry: str = Field(
        description=f"Journal text, 1 to {MAX_ENTRY_LENGTH} characters.",
        examples=["Today I learned FastAPI. It feels great!"],
    )
    mood: Mood = Field(description="How the user feels.", examples=["happy"])

    @field_validator("entry")
    @classmethod
    def validate_entry(cls, value: str) -> str:
        """Strip whitespace and reject empty or overly long entries."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Journal entry cannot be empty.")
        if len(cleaned) > MAX_ENTRY_LENGTH:
            raise ValueError(
                f"Journal entry cannot exceed {MAX_ENTRY_LENGTH} characters "
                f"(got {len(cleaned)})."
            )
        return cleaned

    @field_validator("mood", mode="before")
    @classmethod
    def normalize_mood(cls, value: object) -> object:
        """Accept moods in any case, e.g. "Happy" or " SAD ", like the CLI."""
        if isinstance(value, str):
            return value.strip().lower()
        return value


class JournalEntry(BaseModel):
    """A saved journal entry as returned by the API."""

    id: int
    entry: str
    mood: Mood
    mood_symbol: str = Field(description="ASCII face stored in the CSV, e.g. ':)'.")
    sentiment: Sentiment
    timestamp: str = Field(examples=["2026-09-23 22:45"])

    @classmethod
    def from_csv_row(cls, row: dict) -> "JournalEntry":
        """Convert a raw CSV row (all strings) into a typed entry."""
        mood = SYMBOL_TO_MOOD.get(row["mood"], Mood.neutral.value)
        return cls(
            id=int(row["id"]),
            entry=row["message"],
            mood=mood,
            mood_symbol=row["mood"],
            sentiment=MOOD_SENTIMENTS[mood],
            timestamp=row["timestamp"],
        )


class JournalEntryCreated(BaseModel):
    """Response body for a successful POST /journal."""

    message: str = Field(examples=["Journal entry saved successfully."])
    data: JournalEntry
