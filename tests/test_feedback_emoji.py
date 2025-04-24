"""Testing feedback converting to emoji."""

import pytest

from wordle import Wordle


def test_feedback_to_emoji() -> None:
    """Testing the string is converting to emoji correctly."""
    assert Wordle.feedback_to_emoji("G_YG_") == "🟩⬜🟨🟩⬜"


def test_feedback_to_emoji_invalid_character() -> None:
    """Testing the string when it is invalid."""
    with pytest.raises(ValueError):
        Wordle.feedback_to_emoji("GX_YZ")


def test_feedback_to_emoji_empty_string() -> None:
    """Testing the string when it is empty."""
    assert Wordle.feedback_to_emoji("") == ""
