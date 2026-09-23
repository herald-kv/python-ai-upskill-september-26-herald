"""Journal endpoints: list entries and create new ones."""

from fastapi import APIRouter, HTTPException, Query, status

from src.api.models.journal_model import (
    JournalEntry,
    JournalEntryCreate,
    JournalEntryCreated,
    Sentiment,
)
from src.api.utils.file_handler import add_entry, load_entries
from src.core.config import MOOD_SYMBOLS

router = APIRouter(prefix="/journal", tags=["Journal"])


@router.get("", response_model=list[JournalEntry])
def get_entries(
    sentiment_filter: Sentiment | None = Query(
        default=None,
        description="Only return entries with this sentiment.",
    ),
) -> list[JournalEntry]:
    """Return all journal entries, optionally filtered by sentiment.

    Sentiment comes from the mood: happy = positive, sad = negative,
    neutral = neutral.
    """
    try:
        entries = [JournalEntry.from_csv_row(row) for row in load_entries()]
    except (OSError, KeyError, ValueError) as error:
        # A missing column or non-numeric id means the CSV was edited by hand.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not read the journal file: {error}",
        ) from error

    if sentiment_filter is not None:
        entries = [entry for entry in entries if entry.sentiment == sentiment_filter]
    return entries


@router.post(
    "",
    response_model=JournalEntryCreated,
    status_code=status.HTTP_201_CREATED,
)
def create_entry(payload: JournalEntryCreate) -> JournalEntryCreated:
    """Validate a new entry and its mood, then append it to the CSV."""
    try:
        # Store the ASCII face, exactly as the Day 1 CLI does.
        saved_row = add_entry(payload.entry, MOOD_SYMBOLS[payload.mood.value])
    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save the journal entry: {error}",
        ) from error

    return JournalEntryCreated(
        message="Journal entry saved successfully.",
        data=JournalEntry.from_csv_row(saved_row),
    )
